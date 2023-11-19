#pip install PyExecJS
import execjs
#py test to test the example mta retrieval code
def test_http_request():
    context = execjs.compile(open("mta_retrieval.js").read())
    result = context.call("make_http_request")

    assert "Retrieving Data" in result
    assert "Finished retrieving data" in result