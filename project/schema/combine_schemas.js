// Merge model schema source files
// * using json-schema-ref-parser to build single json tree from yml inputs
// * using ajv for minimal sanity check

var fs = require('fs');
var Ajv = require('ajv');
var refParser = require('json-schema-ref-parser');

var refSchema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$ref": __dirname + "/model.schema.yml"
};

refParser.dereference(refSchema)
  .then(function(schema) {
    var outString = JSON.stringify(schema, null, 2) + '\n';
    //console.log(outString);
    var outFilename = __dirname + '/model.schema.json';
    fs.writeFileSync(outFilename, outString);
    console.log(`Wrote ${outFilename}`);

    // Load test file
    var testFilename = __dirname + '/example_geojson.json';
    var testText = fs.readFileSync(testFilename);
    var testJson = JSON.parse(testText);

    // Validate test file
    var ajv = new Ajv(); // options can be passed, e.g. {allErrors: true}
    var validate = ajv.compile(schema);
    //console.log(`schema: ${JSON.stringify(validate.schema, null, 2)}`);

    // if (!validate) {
    //   console.error(validate.errors);
    // }
    var valid = validate(testJson);
    if (valid) {
      console.log('Test file is valid');
    }
    else {
      console.log(validate.errors);
    }
  })
  .catch(function(err) {
    console.error(err);
  });
