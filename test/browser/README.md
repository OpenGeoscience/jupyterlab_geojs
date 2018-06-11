# Browser Testbed

This folder is used to create a browser.html file for testing data
models passed from kernel code to the lab extension widget.

To build the testbed:
* Compile the browser.pug file

To test the latest source code changes:
* Compile typescript files by running ```jlpm build```
* Build a browser.bundle.js file by executing ```npm run build:browser```.
* Load the resulting browser.html file into, yes, a web browser.
