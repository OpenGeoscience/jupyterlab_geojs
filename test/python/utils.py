'''Common test utility functions
'''
import json
import os

import jsonschema

source_folder = os.path.abspath(os.path.dirname(__file__))
root_folder = os.path.join(source_folder, os.pardir, os.pardir)


test_folder = os.path.join(root_folder, 'test')
data_folder = os.path.join(test_folder, 'data')
model_folder = os.path.join(test_folder, 'models')


# Load schema file
schema = None
schema_folder = os.path.join(root_folder, 'project', 'schema')
schema_file  = os.path.join(schema_folder, 'model.schema.json')
with open(schema_file) as f:
    schema_string = f.read()
schema = json.loads(schema_string)


def validate_model(data_model):
    '''Validates input model against schema

    Raises exception if invalid
    '''
    print('validating against schema:')
    jsonschema.validate(data_model, schema)


def write_model(data_model, filename, folder=model_folder):
    '''Writes data model as json file

    '''
    path = os.path.join(folder, filename)
    data_string = json.dumps(data_model, sort_keys=True)
    #data_string = json.dumps(data, sort_keys=True, indent=2)
    with open(path, 'w') as f:
        f.write(data_string)
        print('Wrote {}'.format(path))
