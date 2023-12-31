/* 
Accessing MTA Real time APIs using API Key
Pass in your API Key with the request using the header x-api-key
Example code is shown below 
*/

/* added function call to be used in test file */
function make_http_request() {
const https = require('https');
https.get(
  "<Feed URI>",
  { headers: { "x-api-key": '<Api Key>'}
  },
  (resp) => {
    resp.on('data', (chunk) => {
      console.log("Receiving Data");
    });
    resp.on('end', () => {
      console.log("Finished receiving data");
    });
  }).on("error", (err) => {
    console.log("Error: " + err.message);
  });
}