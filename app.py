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
#Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

# manage-sub route
@app.route('/admin/manage-subjects')
def manage_subjects():
    return render_template('admin/manage_sub.html')

#upload route
@app.route('/admin/upload')
def upload_content():
    return render_template('admin/upload.html')

if __name__ == '__main__':
    app.run(debug=True)