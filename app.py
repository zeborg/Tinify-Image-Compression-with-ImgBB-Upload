from flask import Flask, jsonify, request
import os
import base64
import tinify
import hashlib
import requests

tinify.key = 'YOUR_TINIFY_API_KEY'

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
  if 'url' in request.args:
    imgurl = request.args['url']
  else:
    return jsonify({"error":"'url' attribute not provided."})
  
  fnhashed = hashlib.new('sha1')
  fnhashed.update(imgurl.encode('utf-8'))
  fnhashed = fnhashed.hexdigest()
  
  tinify.from_url(imgurl).to_file(fnhashed)
  
  with open(fnhashed, 'rb') as source:    
    payload = {
      "key": 'YOUR_IMGBB_API_KEY',
      "image": base64.b64encode(source.read()),
      "expiration": 600
    }
    res = requests.post("https://api.imgbb.com/1/upload", payload).json()
    
  os.remove(fnhashed)
  
  return res

if __name__ == '__main__':
  app.run()
