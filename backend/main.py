from flask import Flask, render_template

# 静的ファイルを返す
app = Flask(__name__, static_folder = '../frontend/dist/static', template_folder = '../frontend/dist')

@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')

def index(path):
  return render_template('index.html')

# サーバを起動する
if __name__ == '__main__':
  app.run()
