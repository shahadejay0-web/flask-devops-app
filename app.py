from prometheus_client import start_http_server, Counter
from flask import Flask

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total Requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello DevOps Monitoring!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
