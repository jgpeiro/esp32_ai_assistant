import urequests as requests

def transcribe( server="192.168.1.105", port=5000, buf=b"" ):
    url = "http://" + server + ":" + str( port ) + "/transcribe"
    resp = requests.post( url, data=buf )
    return resp.text


"""
# PC server code
# Requirements
# pip install git+https://github.com/openai/whisper.git 
# pip install Flask

import time
import base64
import flask
import whisper

# available sizes: base, small, medium
# target: cpu, gpu
model = whisper.load_model( "small", "cpu" ) 

app = flask.Flask("Whisper Server")
@app.route( "/transcribe", methods=["POST"] )
def transcribe():
    buf = flask.request.data
    with open( "tmp.wav", "wb" ) as fl:
        fl.write( buf )
    t0 = time.time()
    result = model.transcribe( "tmp.wav", language="en" )
    text = result["text"]
    t1 = time.time()
    print( t1-t0, text )
    return text

app.run( "192.168.1.105", 5000 ) # Get the IP with ipconfig
print( "done" )
"""