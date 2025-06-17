
from flask import Flask, request, render_template, send_file
import os
from moviepy.editor import ImageSequenceClip
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "")[:2000]
        files = request.files.getlist("images")
        file_paths = []

        for file in files[:10]:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(path)
                file_paths.append(path)

        if file_paths:
            clip = ImageSequenceClip(file_paths, fps=2)
            output_path = os.path.join(OUTPUT_FOLDER, "output_video.mp4")
            clip.write_videofile(output_path, fps=24, codec="libx264", preset="ultrafast")
            return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
