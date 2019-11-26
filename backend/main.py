from flask import Flask, render_template

# Vue.js の静的ファイルを返す
app = Flask(__name__, static_folder = '../frontend/dist/static', template_folder = '../frontend/dist')

# API のルーティングを追加する
from api import blueprint_api
app.register_blueprint(blueprint_api)

@app.route('/', defaults = { 'path': '' })
@app.route('/<path:path>')

def index(path):
  return render_template('index.html')

# サーバを起動する
if __name__ == '__main__':
  app.run()
