import urequests as requests
import ujson as json

def complete( key, prompt, max_tokens, stop ):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization" : "Bearer " + key
    }
    data = {
        "model":       "code-davinci-002",
        "prompt":      prompt,
        "temperature": 0.5,
        "max_tokens":  max_tokens,
        "top_p":       1,
        "frequency_penalty": 0.25,
        "presence_penalty":  0.25,
        "stop":        stop
    }
    
    resp = requests.post(
        url,
        headers=headers,
        data=json.dumps(data)
    )
    
    if( resp.status_code != 200 ):
        print( "resp.status_code != 200", resp.status_code )
        print( "resp.content", resp.content )
        return None, None
    
    completion = resp.json()["choices"][0]["text"]
    status = resp.json()["choices"][0]["finish_reason"]
    return status, completion