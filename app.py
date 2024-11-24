from flask import Flask, render_template, request, jsonify
from bingart import BingArt
from dotenv import load_dotenv
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

# Load the Bing authentication cookie
try:
    BING_AUTH_COOKIE = load_bing_cookie()
    print("[OK] Successfully loaded Bing authentication cookie")
except Exception as e:
    sys.exit(f"Failed to load Bing authentication cookie: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    bing_art = BingArt(auth_cookie_U=BING_AUTH_COOKIE)
    try:
        # Generate images based on the prompt
        results = bing_art.generate_images(prompt)
        images = [img['url'] for img in results['images']]
        return jsonify({'images': images})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        bing_art.close_session()

if __name__ == '__main__':
    app.run(debug=True)
