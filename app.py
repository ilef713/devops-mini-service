import logging
import time
import math
import uuid
from flask import Flask, render_template_string, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


# --- Metrics ---
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["endpoint"]
)



app = Flask(__name__)

# --- Logging structuré ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()
    g.endpoint = request.path
    logger.info(f"[REQ {g.request_id}] Nouvelle requête reçue sur {request.path}")

def compute_values(number):
    square = number * number
    root = math.sqrt(number) if number >= 0 else None
    return square, root


@app.route("/", methods=["GET", "POST"])
def main():
    number = None
    square = None
    root = None

    if request.method == "POST":
        try:
            number = float(request.form.get("number"))
            square, root = compute_values(number)
        except ValueError:
            number = None
            square = None
            root = None

    # HTML moderne avec Bootstrap
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Mini DevOps Service</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
      </head>
      <body class="bg-light">
        <div class="container py-5">
          <div class="card shadow p-4 mb-4">
            <h1 class="card-title">Hello DevOps!</h1>
            <p class="card-text">Status: <span class="badge bg-success">Running</span></p>
          </div>
          <div class="card shadow p-4">
            <h2>Calculs pour un nombre</h2>
            <form method="POST" class="mb-3">
              <div class="input-group">
                <input type="number" step="any" name="number" class="form-control" placeholder="Entrez un nombre" required>
                <button type="submit" class="btn btn-primary">Calculer</button>
              </div>
            </form>
            {% if number is not none %}
            <ul class="list-group">
              <li class="list-group-item">Nombre: {{number}}</li>
              <li class="list-group-item">Carré: {{square}}</li>
              <li class="list-group-item">Racine carrée: {{root}}</li>
            </ul>
            {% endif %}
          </div>
        </div>
      </body>
    </html>
    """
    return render_template_string(html, number=number, square=square, root=root)

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=g.endpoint,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=g.endpoint
    ).observe(duration)

    logger.info(
        f"[REQ {g.request_id}] Réponse envoyée | Status={response.status} | Durée={round(duration*1000,2)} ms"
    )

    return response


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.errorhandler(Exception)
def handle_exception(e):
    ERROR_COUNT.labels(endpoint=request.path).inc()
    logger.error(f"[REQ {g.get('request_id', 'N/A')}] ERREUR: {str(e)}")
    return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
