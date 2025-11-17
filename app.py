import logging
import time
import math
import uuid
from flask import Flask, render_template_string, request, g

# --- Metrics ---
metrics = {
    "request_count": 0,
    "last_request_duration_ms": 0
}


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
    logger.info(f"[REQ {g.request_id}] Nouvelle requête reçue sur {request.path}")

@app.route("/", methods=["GET", "POST"])
def main():
    number = None
    square = None
    root = None

    if request.method == "POST":
        try:
            number = float(request.form.get("number"))
            square = number * number
            root = math.sqrt(number) if number >= 0 else "N/A"
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
    duration = round((time.time() - g.start_time) * 1000, 2)
    logger.info(
        f"[REQ {g.request_id}] Réponse envoyée | Status={response.status} | Durée={duration} ms"
    )
    metrics["request_count"] += 1
    metrics["last_request_duration_ms"] = duration
    return response

@app.route("/metrics")
def metrics_endpoint():
    output = ""
    for key, value in metrics.items():
        output += f"{key} {value}\n"
    return output, 200, {"Content-Type": "text/plain"}
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"[REQ {g.get('request_id', 'N/A')}] ERREUR: {str(e)}")
    return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
