from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the main home page
@app.route('/')
def home():
    # Render and return the index.html template
    return render_template('index.html')

if __name__ == '__main__':
    # Start the Flask development server
    print("Server is starting... Check the terminal for the link!")
    app.run(debug=True)