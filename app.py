from flask import Flask, render_template, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total App Request Count'
)

@app.before_request
def before_request():
    REQUEST_COUNT.inc()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
