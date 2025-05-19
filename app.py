from flask import Flask, render_template, request, send_from_directory
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/removed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        print("No image found in request")
        return 'No file uploaded.', 400

    file = request.files['image']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    try:
        with Image.open(input_path) as img:
            print(f"Image opened: {input_path}")
            output = remove(img)
            filename_wo_ext = os.path.splitext(file.filename)[0]
            output_filename = f'no-bg-{filename_wo_ext}.png'
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            output.save(output_path, format='PNG')
            print(f"Output saved to: {output_path}")

        return {'url': f'/static/removed/{output_filename}'}

    except Exception as e:
        print(f"❌ Error during background removal: {str(e)}")
        return {'error': 'Failed to remove background.'}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # default to 5000 for local
    app.run(debug=False, host='0.0.0.0', port=port)

