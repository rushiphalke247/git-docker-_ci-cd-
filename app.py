import os
from flask import Flask

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 3000))

@app.route('/')
def hello():
    return 'Hello from python-demo-app!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
    print(f'Listening on {PORT}')