import os
import datetime
import socket
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath("t4s")
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)

app.secret_key = "super-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )




# Configure local SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Initialize the database within app context
with app.app_context():
    db.create_all()




@app.route('/')
def home():
    all_notes = Note.query.all()
    files = sorted(os.listdir(app.config["UPLOAD_FOLDER"]))
    return render_template('notes.html', notes=all_notes, files=files)

@app.route('/create', methods=['POST'])
def create_note():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file selected.")
        return redirect(url_for("home"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("home"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("PDF uploaded successfully!")
    else:
        flash("Only PDF files are allowed.")

    return redirect(url_for("home"))


@app.route("/download/<path:filename>")
def download_file(filename):
    # Validate filename to prevent path traversal attacks
    filename = secure_filename(filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
  
    # Check if file exists
    if not os.path.isfile(filepath):
        flash(f"File '{filename}' not found.")
        return redirect(url_for("home"))
        
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )

# Route with a dynamic string parameter
@app.route('/greet/<name>')
def greet(name):
    # Capitalizes the name provided in the URL path
    clean_name = name.capitalize()
    return f"<h1>Hello, {clean_name}!</h1><p>Welcome back to the platform.</p>"

@app.route('/api/v1/details')
def details():
    return jsonify({
        "name": "Davismatrix",
        "version": "1.0.0",
        "description": "A simple Flask application demonstrating dynamic routing and API endpoints.",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    })

@app.route('/api/v1/healthz')
def health():
    return jsonify({
        "status": "healthy",
        "Host": socket.gethostname(),
        "message": "The application is running smoothly and is ready to handle requests.",
        "Environment": "${{values.app_env}}",
        "app_name": "${{values.app_name}}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
