from config import config
from flask import Flask, request, render_template, send_from_directory, abort
from flask_limiter import Limiter
from flask_recaptcha import ReCaptcha
import os
import uuid


app = Flask(__name__)
app.config.from_object(config)
recaptcha = ReCaptcha(app=app)

#Vault directory
app_path = app.root_path
if not os.path.exists(os.path.join(app_path,(config.VAULT_PATH))): os.makedirs(os.path.join(app_path,(config.VAULT_PATH)))

#DDOS mitigation
limiter = Limiter (app, key_func=lambda : request.remote_addr, global_limits=["60/minute" ])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload/<path>', methods=['POST'])
def upload(path):
    innerpath = os.path.join(config.VAULT_PATH, path)
    if 'file' not in request.files:return "NO FILE" #or
    if not os.path.exists(innerpath): return abort(418)
    file     = request.files['file']
    filesize = len(file.read())
    dirsize  = sum([os.path.getsize(os.path.join(innerpath, item)) for item in os.listdir(innerpath)])
    if filesize + dirsize > config.MAX_VAULT_SIZE: return abort(413)
    savepath = os.path.join(config.VAULT_PATH, path, file.filename)
    file.save(savepath)
    return  'ok'

@app.route('/generate', methods=['POST'])
#@limiter.limit("1 per hour")
def generate():
    if recaptcha.verify():
        newdir = str(uuid.uuid4())
        os.mkdir (os.path.join(config.VAULT_PATH, newdir))
        return newdir
    return abort(400)

@app.route('/download/<path>/<filename>', methods=['GET'])
def download(path, filename):
    return send_from_directory (os.path.join(config.VAULT_PATH, path), filename, as_attachment=True)

#TEST recaptcha
@app.route("/submit", methods=["POST"])
def submit():

    if recaptcha.verify(): return "recaptcha SUCCESS"
    else: return "-- FAIL --"

def main():
   app.run(host = config.HOST)

if __name__ == '__main__':
    main()
