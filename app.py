from flask import Flask, render_template, request, jsonify
from bingart import BingArt
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import sys

def load_bing_cookie():
    """Load and validate the Bing authentication cookie from environment variables."""
    # Ensure .env file exists
    if not os.path.exists('.env'):
        sys.exit("Error: .env file not found. Please create a .env file with your BING_AUTH_COOKIE.")
    
    # Load environment variables
    load_dotenv()
    
    # Get the auth cookie
    cookie = os.getenv('BING_AUTH_COOKIE')
    
    if not cookie:
        sys.exit("Error: BING_AUTH_COOKIE not found in .env file. Please add your Bing authentication cookie.")
    
    if len(cookie) < 50:  # Basic validation for cookie length
        sys.exit("Error: BING_AUTH_COOKIE appears to be invalid (too short). Please check your cookie value.")
    
    return cookie

# Initialize Flask app
app = Flask(__name__)

# Ensure the instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

# Configure SQLite database with absolute path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'history.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the ImageHistory model
class ImageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(500), nullable=False)
    images = db.Column(db.Text, nullable=False)  # Store as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        try:
            # Safely parse the JSON string
            images = json.loads(self.images)
            return {
                'id': self.id,
                'prompt': self.prompt,
                'images': images,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        except json.JSONDecodeError as e:
            print(f"Error decoding images JSON for entry {self.id}: {e}")
            return {
                'id': self.id,
                'prompt': self.prompt,
                'images': [],
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

# Create database tables and load authentication
with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print("[OK] Database tables created successfully")
        
        # Load authentication cookie
        BING_AUTH_COOKIE = load_bing_cookie()
        print("[OK] Successfully loaded Bing authentication cookie")
        
        # Verify database connection by trying to query
        test_query = ImageHistory.query.first()
        print("[OK] Database connection verified")
    except Exception as e:
        sys.exit(f"Failed to initialize application: {str(e)}")

@app.route('/')
def index():
    """Render the home page with history."""
    try:
        # Get the last 10 image generations, ordered by most recent first
        history = ImageHistory.query.order_by(ImageHistory.created_at.desc()).limit(10).all()
        history_data = [entry.to_dict() for entry in history]
        print(f"[INFO] Loaded {len(history_data)} history entries")
        return render_template('index.html', history=history_data)
    except Exception as e:
        print(f"Error loading history: {str(e)}")
        return render_template('index.html', history=[])

@app.route('/generate', methods=['POST'])
def generate():
    """Generate images from a prompt and store in history."""
    try:
        prompt = request.form.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        bing_art = BingArt(auth_cookie_U=BING_AUTH_COOKIE)
        try:
            # Generate images based on the prompt
            results = bing_art.generate_images(prompt)
            images = [img['url'] for img in results['images']]

            # Store in history using proper JSON serialization
            history_entry = ImageHistory(
                prompt=prompt,
                images=json.dumps(images)  # Properly serialize list to JSON string
            )
            db.session.add(history_entry)
            db.session.commit()
            print(f"[INFO] Saved new history entry with {len(images)} images")

            return jsonify({
                'images': images,
                'history_entry': history_entry.to_dict()
            })
        except Exception as e:
            print(f"Error generating images: {str(e)}")
            return jsonify({'error': str(e)}), 500
        finally:
            bing_art.close_session()

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
