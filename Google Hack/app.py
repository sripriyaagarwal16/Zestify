from flask import Flask, render_template, request, jsonify
import os
from recommendation_sys import generate_recommendations

app = Flask(__name__)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')  # Assumes the HTML file is saved as templates/index.html

# Route to handle form submission and image upload
@app.route('/recommend', methods=['POST'])
def recommend():
    disease = request.form['disease']
    
    # Get the uploaded file
    if 'imageUpload' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['imageUpload']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save the uploaded file
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_path)
    
    # Generate recommendations using the recommendation system
    recommendations = generate_recommendations(disease, image_path)
    
    # Return recommendations as JSON
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
