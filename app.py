from flask import Flask, render_template, request, redirect, session, send_file, abort #type: ignore
from flask_mysqldb import MySQL #type: ignore
from werkzeug.security import generate_password_hash, check_password_hash #type: ignore
from werkzeug.utils import secure_filename #type: ignore
import os

app = Flask(__name__)

app.secret_key = "lara" # Change this to a random secret key in production

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "YOUR_MYSQL_PASSWORD"
app.config["MYSQL_DB"] = "file_storage"

mysql = MySQL(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def logged_in():
    return "user_id" in session


@app.route("/")
def home():
    if logged_in():
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(%s,%s)",
                (username, hashed_password)
            )
            mysql.connection.commit()
        except:
            return "Username already exists"
        finally:
            cur.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT id,password FROM users WHERE username=%s",
            (username,)
        )

        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if not logged_in():
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT id,filename,upload_time FROM files WHERE user_id=%s",
        (session["user_id"],)
    )

    files = cur.fetchall()
    cur.close()

    return render_template("dashboard.html", files=files)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not logged_in():
        return redirect("/login")

    if request.method == "POST":
        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        if not allowed_file(file.filename):
            return "File type not allowed"

        filename = secure_filename(file.filename)

        user_folder = os.path.join(UPLOAD_FOLDER, str(session["user_id"]))
        os.makedirs(user_folder, exist_ok=True)

        filepath = os.path.join(user_folder, filename)

        file.save(filepath)

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO files(user_id,filename,filepath) VALUES(%s,%s,%s)",
            (session["user_id"], filename, filepath)
        )

        mysql.connection.commit()
        cur.close()

        return redirect("/dashboard")

    return render_template("upload.html")


@app.route("/download/<int:file_id>")
def download(file_id):
    if not logged_in():
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT filepath FROM files WHERE id=%s AND user_id=%s",
        (file_id, session["user_id"])
    )

    file = cur.fetchone()
    cur.close()

    if not file:
        abort(403)

    return send_file(file[0], as_attachment=True)


if __name__ == "__main__":
    app.run()