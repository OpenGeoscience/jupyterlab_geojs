'''A set of classes to support point cloud features derived from
   LAS/LAZ input data.
'''

import os
import pkg_resources
import struct
import sys
import uuid

class LASHeader:
    '''Data representing LAS public header block

    '''
    def __init__(self):
        # In public header block order:
        self.file_signature = None
        self.file_source_id = None
        self.global_encoding = None
        self.project_guid = None
        self.version_major = None
        self.version_minor = None
        self.system_identifier = None
        self.generating_software = None
        self.file_creation_doy = None  # (day of year)
        self.file_creation_year = None
        self.header_size = None
        self.offset_to_points = None
        self.number_of_vlr = None
        self.point_data_record_format = None
        self.point_data_record_length = None
        self.legacy_point_count = None
        self.legacy_number_of_points_by_return = None
        self.x_scale_factor = None
        self.y_scale_factor = None
        self.z_scale_factor = None
        self.x_offset = None
        self.y_offset = None
        self.z_offset = None
        self.max_x = None
        self.min_x = None
        self.max_y = None
        self.min_y = None
        self.max_z = None
        self.min_z = None

        # Version 1.3:
        self.start_of_waveform_packet_records = None

        # Version 1.4:
        self.evlr_offset = None
        self.evlr_length = None
        self.number_of_point_records = None
        self.number_of_points_by_return = None

    def __str__(self):
        '''Generates a string listing all of the contents

        Does not include values that aren't initialized
        '''
        data_list = list()
        for key, value in sorted(self.__dict__.items()):
            if value is None:
                continue

            if key in ['global_encoding']:
                data_list.append('  {}: 0x{:x}'.format(key, value))
            else:
                data_list.append('  {}: {}'.format(key, value))
        data_string = '\n'.join(data_list)
        return '{{\n{}\n}}'.format(data_string)



class LASMetadata:
    '''Store for metadata extracted from LAS/LAZ file

    '''
    def __init__(self):
        self.header = None
        self.projection_wkt = None


class LASParser:
    '''Parser for LAS/LAZ header and vlr blocks

    '''
    def __init__(self):
        ''''''
        self._header = None  # LASHeader
        self._projection_wkt = None

    def parse(self, f):
        '''Parses LAS/LAZ header and vlr blocks

        @param f: input stream object
        Returns new LASMetadata instance.
        '''
        self._header = self._parse_header(f)

        # Update projection WKT by parsing VLR data
        self._projection_wkt = None
        self._parse_vlrs(f)

        # Parse instream here

        metadata = LASMetadata()
        metadata.header = self._header
        metadata.projection_wkt = self._projection_wkt
        return metadata

    def _parse_header(self, f):

        '''Reads public header block

        Uses brute force to unpack the contents.
        Sets input file pointer to the end of the header.
        '''
        h = LASHeader()

        # Read up to header size field
        first_block_size = 96

        f.seek(0, 0)   # make sure stream is reset
        blob = f.read(first_block_size)
        pos = 0

        h.file_signature = struct.unpack_from('4s', blob, pos)[0]
        pos += 4
        if h.file_signature != 'LASF'.encode():
            raise Exception('Not a LAS/LAZ file.  Invalid file signature.')

        h.file_source_id,h.global_encoding = struct.unpack_from('HH', blob, pos)
        pos += 4

        h.project_guid = uuid.UUID(bytes=blob[pos:pos+16])
        pos += 16

        h.version_major,h.version_minor = struct.unpack_from('BB', blob, pos)
        pos += 2

        sys_id = struct.unpack_from('32s', blob, pos)[0]
        h.system_identifier = str(sys_id, encoding='ascii')
        pos += 32

        gen_sw = struct.unpack_from('32s', blob, pos)[0]
        h.generating_software = str(gen_sw, encoding='ascii')
        pos += 32

        h.file_creation_doy,h.file_creation_year = struct.unpack_from('HH', blob, pos)
        pos += 4

        h.header_size = struct.unpack_from('H', blob, pos)[0]
        pos += 2
        #print('header size {}, currently at pos {}'.format(h.header_size, pos))


        # Read rest of header and reset pos
        next_block_size = h.header_size - first_block_size
        blob = f.read(next_block_size)
        pos = 0


        h.offset_to_points = struct.unpack_from('I', blob, pos)[0]
        pos += 4

        h.number_of_vlr = struct.unpack_from('I', blob, pos)[0]
        pos += 4

        h.point_data_record_format,h.point_data_record_length = struct.unpack_from('BH', blob, pos)
        pos += 3

        h.legacy_point_count = struct.unpack_from('I', blob, pos)[0]
        pos += 4

        h.legacy_number_of_points_by_return = struct.unpack_from('IIIII', blob, pos)
        pos += 20

        h.x_scale_factor,h.y_scale_factor,h.z_scale_factor = struct.unpack_from('ddd', blob, pos)
        pos += 24
        h.x_offset,h.y_offset,h.z_offset = struct.unpack_from('ddd', blob, pos)
        pos += 24

        h.max_x,h.min_x,h.max_y,h.min_y,h.max_z,h.min_z = struct.unpack_from('dddddd', blob, pos)
        pos += 48

        if h.version_major >= 1 and h.version_minor >= 3:
            h.start_of_waveform_packet_records = struct.unpack_from('Q', blob, pos)[0]
            pos += 8
            #print('Block1.3 pos', pos)

        if h.version_major >= 1 and h.version_minor >= 4:
            h.evlr_offset,h.evlr_length = struct.unpack_from('QI', blob, pos)
            pos += 12

            h.number_of_point_records = struct.unpack_from('Q', blob, pos)[0]
            pos += 8

            h.number_of_points_by_return = struct.unpack_from('QQQQQ', blob, pos)
            pos += 40

        #print('Final pos', pos)
        self._header = h
        return h

    def _parse_vlrs(self, f):
        '''Read variable length records looking for spatial coord system

        NOTE: The input file refernce (f) MUST be set to the start of the VLR records
        '''
        # Initialize Struct to unpack VLR headers
        vlr_header_struct = struct.Struct('H16sHH32s')
        #print('vlr_header_struct.size: {}'.format(vlr_header_struct.size))
        for i in range(self._header.number_of_vlr):
            block = f.read(vlr_header_struct.size)
            vlr_header_tuple = vlr_header_struct.unpack(block)
            #print('vlr_header_tuple {}'.format(i+1))

            reserved, user_id_bytes, record_id, record_length, description_bytes = \
                vlr_header_tuple
            # Convert text items (bytes to string)
            user_id = self._bytes_to_string(user_id_bytes)
            description = self._bytes_to_string(description_bytes)
            # print('  user_id:       {}'.format(user_id))
            # print('  record_id:     {}'.format(record_id))
            # print('  record_length: {}'.format(record_length))
            # print('  descripton:    {}'.format(description))

            # Read record 2112 to get coord system wkt
            if user_id == 'LASF_Projection' and record_id == 2112:
                payload = f.read(record_length)
                self._projection_wkt = self._bytes_to_string(payload)
                # print('coord_sys wkt:')
                # print(self._projection_wkt)
                # print()

            # Otherwise skip over
            else:
                f.seek(record_length, 1)
                # payload = f.read(record_length)

    def _bytes_to_string(self, input_bytes, rstrip=True, encoding='ascii'):
        '''Convert input bytes to ascii string

        @param: rstrip (boolean) if true, remove terminating null bytes
        '''
        if rstrip:
            # Remove trailing zeros (https://stackoverflow.com/a/5076070)
            input_bytes = input_bytes.split(b'\0',1)[0]
        output_string = str(input_bytes, encoding=encoding)
        return output_string


# Transcribe point attribute names for point data record formats,
# as of July 2018, LAS version 1.4, per https://www.asprs.org
# Transcribed by hand, so user beware
LASPointAttributes = dict()
LASPointAttributes[0] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Scan Direction Flag',
    'Edge of Flight Line', 'Classification',
    'Scan Angle Rank (-90 to +90) – Left side', 'User Data'
    )
LASPointAttributes[1] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Scan Direction Flag',
    'Edge of Flight Line', 'Classification',
    'Scan Angle Rank (-90 to +90) – Left side', 'User Data',
    'Point Source ID', 'GPS Time'
    )

LASPointAttributes[2] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Scan Direction Flag',
    'Edge of Flight Line', 'Classification',
    'Scan Angle Rank (-90 to +90) – Left side', 'User Data',
    'Point Source ID', 'Red', 'Green', 'Blue'
    )
LASPointAttributes[3] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Scan Direction Flag',
    'Edge of Flight Line', 'Classification',
    'Scan Angle Rank (-90 to +90) – Left side', 'User Data',
    'Point Source ID', 'GPS Time', 'Red', 'Green', 'Blue'
    )
LASPointAttributes[4] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Scan Direction Flag',
    'Edge of Flight Line', 'Classification',
    'Scan Angle Rank (-90 to +90) – Left side', 'User Data',
    'Point Source ID', 'GPS Time', 'Wave Packet Descriptor Index',
    'Byte offset to waveform data', 'Return Point Waveform Location',
    'X(t)', 'Y(t)', 'Z(t)'
    )
LASPointAttributes[5] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Scan Direction Flag',
    'Edge of Flight Line', 'Classification',
    'Scan Angle Rank (-90 to +90) – Left side', 'User Data',
    'Point Source ID', 'GPS Time', 'Red', 'Green', 'Blue',
    'Wave Packet Descriptor Index', 'Byte offset to waveform data',
    'Return Point Waveform Location', 'X(t)', 'Y(t)', 'Z(t)'
    )
LASPointAttributes[6] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Classification Flags',
    'Scanner Channel', 'Scan Direction Flag', 'Edge of Flight Line',
    'Classification', 'User Data', 'Scan Angle', 'Point Source ID',
    'GPS Time'
    )
LASPointAttributes[7] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Classification Flags',
    'Scanner Channel', 'Scan Direction Flag', 'Edge of Flight Line',
    'Classification', 'User Data', 'Scan Angle',  'Point Source ID',
    'GPS Time', 'Red', 'Green', 'Blue'
    )
LASPointAttributes[8] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Classification Flags',
    'Scanner Channel', 'Scan Direction Flag', 'Edge of Flight Line',
    'Classification', 'User Data', 'Scan Angle',  'Point Source ID',
    'GPS Time', 'Red', 'Green', 'Blue', 'NIR'
    )
LASPointAttributes[9] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Classification Flags',
    'Scanner Channel', 'Scan Direction Flag', 'Edge of Flight Line',
    'Classification', 'User Data', 'Scan Angle',  'Point Source ID',
    'GPS Time', 'Wave Packet Descriptor Index',
    'Byte offset to waveform data', 'Return Point Waveform Location',
    'X(t)', 'Y(t)', 'Z(t)'
    )
LASPointAttributes[10] = (
    'X', 'Y', 'Z', 'Intensity', 'Return Number',
    'Number of Returns (given pulse)', 'Classification Flags',
    'Scanner Channel', 'Scan Direction Flag', 'Edge of Flight Line',
    'Classification', 'User Data', 'Scan Angle',  'Point Source ID',
    'GPS Time', 'Red', 'Green', 'Blue', 'NIR',
    'Wave Packet Descriptor Index', 'Byte offset to waveform data',
    'Return Point Waveform Location', 'X(t)', 'Y(t)', 'Z(t)'
    )
