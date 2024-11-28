from app import app  # Import the Flask app from the `app/app.py` file

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)