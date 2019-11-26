from flask import Flask, render_template

from api import api_blueprint

# Vue.js の静的ファイルを返す
app = Flask(__name__, static_folder = '../frontend/dist/static', template_folder = '../frontend/dist')
# API のルーティングを追加する
app.register_blueprint(api_blueprint)

@app.route('/', defaults = { 'path': '' })
@app.route('/<path:path>')

def index(path):
  return render_template('index.html')

# サーバを起動する
if __name__ == '__main__':
  app.run()
