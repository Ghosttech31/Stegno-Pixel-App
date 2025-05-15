from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash, send_from_directory
from steg_crypto import encrypt_message, decrypt_message, embed_message_in_image, extract_message_from_image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import json
import os

UPLOAD_FOLDER = 'static/uploads'
ENCODED_FOLDER = 'static/encoded'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCODED_FOLDER, exist_ok=True)


app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.secret_key = "your_super_secret_key_here"

# Helper Functions

def get_user_by_username(username):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []
    except json.JSONDecodeError:
        users = []

    if isinstance(users, dict):
        user = users.get(username)
        if user:
            return {"username": username, "password": user.get("password")}
    else:
        for user in users:
            if isinstance(user, dict) and user.get("username") == username:
                return user
    return None

def save_user(username, hashed_password):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if not isinstance(users, dict):
        users = {}

    users[username] = {"password": hashed_password}

    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def log_event(user_id, action):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"UserID:{user_id} - {action} at {timestamp}\n"
    with open("logs.txt", "a") as f:
        f.write(log_line)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Routes

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/encode", methods=["GET", "POST"])
@login_required
def encode():
    result = None
    error = None
    encoded_filename = None

    if request.method == "POST":
        try:
            image_file = request.files.get("image")
            message = request.form.get("message")
            password = request.form.get("password")

            if not image_file or not image_file.filename:
                raise ValueError("No image file selected")
            if not message:
                raise ValueError("No message provided")
            if not password:
                raise ValueError("No password provided")

            filename = secure_filename(image_file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(input_path)

            encrypted_message = encrypt_message(message, password)
            encoded_filename = f"encoded_{filename}"
            output_path = os.path.join(ENCODED_FOLDER, encoded_filename)
            embed_message_in_image(input_path, encrypted_message, output_path)

            result = "Message encoded and embedded successfully!"
        except Exception as e:
            error = f"Encoding failed: {str(e)}"

    return render_template("encode.html", result=result, error=error, encoded_filename=encoded_filename)

@app.route("/decode", methods=["GET", "POST"])
@login_required
def decode():
    decoded_message = None
    error = None

    if request.method == "POST":
        try:
            image_file = request.files.get("image")
            password = request.form.get("password")

            if not image_file or not image_file.filename:
                raise ValueError("No image file selected")
            if not password:
                raise ValueError("No password provided")

            filename = secure_filename(image_file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(input_path)

            encrypted_message = extract_message_from_image(input_path)
            decoded_message = decrypt_message(encrypted_message, password)
        except Exception as e:
            error = f"Decoding failed: {str(e)}"

    return render_template("decode.html", decoded_message=decoded_message, error=error)

@app.route("/download/<filename>")
@login_required
def download(filename):
    return send_from_directory(ENCODED_FOLDER, filename, as_attachment=True)

@app.route("/mylogs")
@login_required
def my_logs():
    user_id = session["user_id"]
    user_logs = []

    try:
        with open("logs.txt", "r") as f:
            for line in f:
                if f"UserID:{user_id}" in line:
                    user_logs.append(line.strip())
    except FileNotFoundError:
        user_logs = []

    return render_template("mylogs.html", logs=user_logs)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if get_user_by_username(username):
            flash("Username already taken.", "error")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)
        save_user(username, hashed_password)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

        if user and check_password_hash(user.get("password", ""), password):
            session["user_id"] = user.get("username")
            log_event(user.get("username"), "User logged in")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    user = session.pop("user_id", None)
    if user:
        log_event(user, "User logged out")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
