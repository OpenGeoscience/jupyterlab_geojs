## Data model for jupyterlab_geojs

This folder contains the files associated with the internal
representation used to send data from the notebook kernel to the GeoJS
web client. Because GeoJS has a large API, a formal schema is used to
specify the interface.

The "source" files are authored in YAML, using the .yml extension.
The entry point for the source is file model.schema.yml.

For development, the node script combine_schemas.js is used to load the
.yml files and generate a single json-schema file, model.schema.json.
This file is used in conjunction with testing the notebook (python)
code that generates data to send to the web client.
