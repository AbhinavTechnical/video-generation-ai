
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = ""
    uploaded_filenames = []

    if request.method == 'POST':
        images = request.files.getlist('images')
        prompt = request.form.get('prompt', '')

        if len(images) == 0 or prompt.strip() == "":
            return render_template('index.html', result="❌ Please upload at least one image and enter a prompt.")

        if len(images) > 10:
            return render_template('index.html', result="⚠️ Maximum 10 images allowed.")

        if len(prompt) > 2000:
            return render_template('index.html', result="⚠️ Prompt too long. Max 2000 characters allowed.")

        for image in images:
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                uploaded_filenames.append(filename)

        # Simulated Video Generation (replace with actual AI logic or Replicate API)
        result_text = f"✅ Video generation started for {len(images)} images with prompt: {prompt[:80]}... (truncated)"
        # result_video = generate_video(images, prompt) <-- to be implemented

    return render_template('index.html', result=result_text, filenames=uploaded_filenames)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
