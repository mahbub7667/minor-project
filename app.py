from flask import Flask, render_template

app = Flask(__name__)

#Home Page Route
@app.route('/')
def home():
    return render_template('index.html')

#Register Page Route
@app.route('/register')
def register():
    return render_template('register.html')

# LOGIN Page Route
@app.route('/login')
def login():
    return render_template('login.html')

#Student Dashboard Route
@app.route('/student/dashboard')
def student_dashboard():
    # Note how we point to the file inside the student folder
    return render_template('student/dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)