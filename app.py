import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Configuration
IMAGE_FOLDER = './Exit1' 
ROWS = 8
COLS = 8

@app.route('/')
def index():
    # Initialize a list with 64 empty slots
    tiles = [None] * (ROWS * COLS)
    
    if os.path.exists(IMAGE_FOLDER):
        # Filter for only .jpg files that start with 'tile_'
        files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith('.jpg') and f.startswith('tile_')]
        
        for filename in files:
            try:
                # Extract number from 'tile_NN.jpg'
                # Splits by '_' then by '.' to get the digits
                parts = filename.split('_')
                if len(parts) >= 2:
                    num_str = parts[1].split('.')[0]
                    num = int(num_str)
                    
                    # Place in 0-indexed list (tile_1 goes to index 0)
                    if 1 <= num <= 64:
                        tiles[num - 1] = filename
            except (ValueError, IndexError):
                continue

    return render_template('index.html', tiles=tiles)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    app.run(debug=True, port=5001)