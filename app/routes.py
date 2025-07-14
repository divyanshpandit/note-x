from flask import (
    Blueprint, render_template, request, redirect,
    url_for, send_file, jsonify
)
from tasks import start_generate_notes_task, get_task_result

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        task_id = start_generate_notes_task(topic)

        # AJAX (fetch) submit → return JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(task_id=task_id)

        # Normal form submit → redirect
        return redirect(url_for("main.status", task_id=task_id))

    return render_template("index.html")

@main.route("/status/<task_id>")
def status(task_id):
    return render_template("status.html", task_id=task_id)

@main.route("/api/status/<task_id>")
def api_status(task_id):
    state, data = get_task_result(task_id)
    return jsonify(state=state, result=data)

@main.route("/download/<task_id>")
def download(task_id):
    state, data = get_task_result(task_id)
    if state != "SUCCESS":
        return "File not ready", 404
    return send_file(data["pdf_path"], as_attachment=True)
