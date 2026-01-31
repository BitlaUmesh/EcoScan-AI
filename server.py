from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import base64
from io import BytesIO
from PIL import Image

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.utils import run_complete_analysis, load_image_from_bytes

app = Flask(__name__, template_folder='frontend', static_folder='frontend/static')
CORS(app)

# Configure max upload size (100MB) to handle high-res camera captures
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if hasattr(e, "code"):
        return jsonify(error=str(e)), e.code
    # Handle non-HTTP errors
    return jsonify(error=str(e)), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files and 'image_base64' not in request.form:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        if 'image' in request.files:
            print("Received file upload")
            file = request.files['image']
            image_bytes = file.read()
        else:
            print("Received base64 image")
            # Handle base64 image from camera
            image_data = request.form['image_base64']
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)

        print(f"Image bytes length: {len(image_bytes)}")
        image = load_image_from_bytes(image_bytes)
        if image is None:
            print("Failed to load image from bytes")
            return jsonify({'error': 'Invalid image data'}), 400

        # Run analysis
        print("Starting analysis...")
        vision_result, analysis_result, final_output = run_complete_analysis(image)
        print("Analysis complete")
        
        # Convert image to base64 for response if needed, or just return results
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        response_status = final_output.get('status', 'success')
        
        return jsonify({
            'status': response_status,
            'results': final_output,
            'image_b64': img_str,
            'vision': vision_result,
            'analysis': analysis_result,
            'error': final_output.get('error')
        })

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting EcoScan AI Server...")
    print("Go to http://localhost:5000 to use the HTML frontend")
    # Disable debug mode for stability during testing to prevent reloads
    app.run(debug=False, host='0.0.0.0', port=5000)
