import boto3
import uuid

from flask import Flask, redirect, url_for, request, render_template

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            uploaded_file = request.files["file-to-save"]
            if not allowed_file(uploaded_file.filename):
                return "FILE NOT ALLOWED!"

            new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.', 1)[1].lower()

            bucket_name = "cloudgroup2"
            s3 = boto3.resource("s3", aws_access_key_id=YOUR_ACCESS_KEY,aws_secret_access_key=YOUR_AWS_SECRET_KEY)
            s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)


            return redirect(url_for("index"))

        return render_template("index.html")

    return app
