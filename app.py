
from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files or 'prompt' not in request.form:
            return render_template('index.html', result="Missing image or prompt")

        image = request.files['image']
        prompt = request.form['prompt']

        if image.filename == '':
            return render_template('index.html', result="No image selected")

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

        # ✅ This is where your AI logic would go (for now, just dummy success)
        result_text = f"Video generation started for: {image.filename} with prompt: {prompt[:50]}..."

        return render_template('index.html', result=result_text)

    return render_template('index.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


