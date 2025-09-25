import os
from flask import Flask, jsonify

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 3000))

@app.route('/')
def hello():
    return 'Hello from python-demo-app!'

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running successfully',
        'version': '1.0.0'
    })

@app.route('/info')
def info():
    """Application info endpoint"""
    return jsonify({
        'app_name': 'python-demo-app',
        'version': '1.0.0',
        'description': 'Simple Flask app with CI/CD pipeline',
        'endpoints': {
            '/': 'Hello message',
            '/health': 'Health check',
            '/info': 'Application information'
        }
    })

if __name__ == '__main__':
    print(f'🚀 Starting Python Demo App on port {PORT}')
    print(f'📍 Health check: http://localhost:{PORT}/health')
    print(f'📍 App info: http://localhost:{PORT}/info')
    app.run(host='0.0.0.0', port=PORT, debug=False)