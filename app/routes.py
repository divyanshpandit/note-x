# app/routes.py
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, send_file, jsonify
)
from celery.result import AsyncResult

main = Blueprint("main", __name__)

# ───────────────── Home page ───────────────── #
@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]

        # defer import to avoid circular dependency
        from tasks import generate_notes_task
        task = generate_notes_task.delay(topic)

        # If called via fetch (AJAX), return JSON with task_id
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(task_id=task.id), 202

        # Fallback for plain form posts (should rarely happen now)
        return redirect(url_for("main.status", task_id=task.id))

    return render_template("index.html")

# ───────────────── Status page ───────────────── #
@main.route("/status/<task_id>")
def status(task_id):
    return render_template("status.html", task_id=task_id)

# JSON status endpoint
@main.route("/api/status/<task_id>")
def api_status(task_id):
    task = AsyncResult(task_id)
    return jsonify(
        state=task.state,
        result=task.result or {},
        error=str(task.info) if task.failed() else None,
    )

# Download endpoint
@main.route("/download/<task_id>")
def download(task_id):
    task = AsyncResult(task_id)
    return send_file(task.result["pdf_path"], as_attachment=True)
