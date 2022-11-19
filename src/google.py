import time
import urequests as requests
import ujson as json
import ubinascii as binascii

def replace_non_ascii_chars( text ):
    text = text.replace( "á", "a" )
    text = text.replace( "é", "e" )
    text = text.replace( "í", "i" )
    text = text.replace( "ó", "o" )
    text = text.replace( "ú", "u" )
    text = text.replace( "ñ", "n" )
    
    text = text.replace( "Á", "A" )
    text = text.replace( "É", "E" )
    text = text.replace( "Í", "I" )
    text = text.replace( "Ó", "O" )
    text = text.replace( "Ú", "U" )
    text = text.replace( "Ñ", "N" )
    return text

def recognize( key, fl_name ):
    url_recognize = "https://speech.googleapis.com/v1/speech:recognize?key=" + key
    with open( fl_name, "rb" ) as fl:
        buf = fl.read()
    headers = { "Content-Type": "application/json" }
    data = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 8000,
            "languageCode": "es-ES"
            #"languageCode": "en-US"
        },
        "audio": {
            "content": binascii.b2a_base64( buf )[:-1].decode( "utf-8" )
        }
    }
    resp = requests.post( url_recognize, headers=headers, json=data )
    if( resp.status_code != 200 ):
        print( "resp.status_code != 200", resp.status_code )
        print( "resp.content", resp.content )
        return None
    
    results = resp.json()["results"]
    transcript = "".join([result["alternatives"][0]["transcript"] for result in results])
    return transcript

def translate( key, text ):
    text = replace_non_ascii_chars( text )
    url = "https://translation.googleapis.com/language/translate/v2?key=" + key
    data = {
        "q": text,
        #"source": "es",
        "target": "en",
        "format": "text",
        "key": key
    }
    resp = requests.post( url, json=data )
    if( resp.status_code != 200 ):
        print( "resp.status_code != 200", resp.status_code )
        print( "resp.content", resp.content )
        return None
    
    return resp.json()["data"]["translations"][0]["translatedText"]

