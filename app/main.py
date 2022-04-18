import os
from flask import request, Flask
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = os.path.join('app', 'public')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_folder='public')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def response(message, status=200, mimetype='application/json'):
  if(mimetype == 'application/json'):
    return app.response_class(
      response=json.dumps(message),
      status=status,
      mimetype='application/json'
    )
  else:
    return app.response_class(
      response=message,
      status=status
    )

@app.route('/upload', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return response({"success": False, "message": "Envie um arquivo na chave file"}, 400)
    file = request.files['file']
    if file.filename == '':
      return response({"success": False, "message": "Envie um arquivo."}, 400)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return response({"success": True}, 201)
    return response({"success": False, "message": "Arquivo não encontrado ou não suportado."}, 400)

@app.route("/")
def home_view():
  return "<h1>Teste de API</h1>"