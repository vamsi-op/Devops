# app.py
# Main Flask application for the Student Feedback System.

from flask import Flask, redirect, render_template, request, url_for

from database import add_feedback, get_all_feedback, get_recent_feedback, init_db

# Flask needs explicit template/static paths because templates and static
# folders are at project root (as requested in the project structure).
app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route("/")
def index():
    """Show the feedback form and recent feedback entries."""
    recent_feedback = get_recent_feedback(limit=5)
    return render_template("index.html", recent_feedback=recent_feedback)


@app.route("/submit", methods=["POST"])
def submit_feedback():
    """Receive feedback form data and store it in SQLite."""
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    # Store only valid, non-empty submissions.
    if name and message:
        add_feedback(name, message)

    return redirect(url_for("feedback"))


@app.route("/feedback")
def feedback():
    """Display all feedback entries."""
    all_feedback = get_all_feedback()
    return render_template("feedback.html", feedback_entries=all_feedback)


if __name__ == "__main__":
    # Initialize database/table before starting the web server.
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
