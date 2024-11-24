# 🎨 Bing Image Generator Web App

> A sleek, dark-themed web application that generates AI images using Bing Image Creator (DALL-E). Built with Flask and modern web technologies.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A Flask-based web application that generates images using Bing's Image Creator (powered by DALL-E). This application provides a simple and intuitive interface to generate AI images from text prompts.

## Features

- Clean and modern dark-themed UI
- Real-time image generation using Bing Image Creator
- Responsive design that works on both desktop and mobile
- Secure environment variable configuration
- Simple and intuitive user interface

## Prerequisites

- Python 3.7+
- A valid Bing authentication cookie
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bing-image-generator.git
cd bing-image-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Bing authentication cookie:
```
BING_AUTH_COOKIE=your_bing_cookie_here
```

To get your Bing authentication cookie:
1. Go to Bing Image Creator
2. Log in to your account
3. Open browser developer tools (F12)
4. Go to Network tab
5. Find the '_U' cookie value
6. Copy this value into your .env file

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter your prompt in the text field and click "Generate" to create images

## Project Structure

```
web/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── static/
│   └── styles.css     # CSS styles for the web interface
└── templates/
    └── index.html     # HTML template for the web interface
```

## Security Notes

- The `.env` file containing your Bing authentication cookie is excluded from the repository via `.gitignore`
- Never commit sensitive credentials to the repository
- Keep your authentication cookie private and secure

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
