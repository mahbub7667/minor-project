import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import supabase 


app = Flask(__name__)
app.secret_key = "smart_study_secret_key"

# Home Page Route
@app.route('/')
def home(): 
    try:
        # Fetching dynamic counts for the landing page
        subjects = supabase.table("subjects").select("id", count="exact").execute()
        resources = supabase.table("resources").select("id", count="exact").execute()
        
        sub_count = subjects.count if subjects.count else 0
        res_count = resources.count if resources.count else 0
    except Exception as e:
        print(f"Error fetching landing stats: {e}")
        sub_count, res_count = 0, 0

    # Ensure this matches your template filename
    return render_template('index.html', sub_count=sub_count, res_count=res_count)


# Register Page Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 1. Decide the role based on email
        if email == "mahbubgaming024@gmail.com":
            assigned_role = "admin"
        else:
            assigned_role = "student"
            
        hashed_password = generate_password_hash(password)
        
        try:
            user_data = {
                "full_name": full_name,
                "email": email,
                "password": hashed_password,
                "role": assigned_role # Now using the dynamic role
            }
            
            supabase.table("users").insert(user_data).execute()
            print(f"User registered as {assigned_role}")
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Registration Error: {e}")
            return "Registration failed."
            
    return render_template('register.html')

# Updated LOGIN Page Route (Replaces your old simple route)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Search for the user in Supabase by email
            response = supabase.table("users").select("*").eq("email", email).execute()
            user_data = response.data

            if user_data:
                user = user_data[0] # Get user from the list
                
                # Check if the provided password matches the hashed password in DB
                if check_password_hash(user['password'], password):
                    # Store user details in session for persistent login
                    session['user_id'] = user['id']
                    session['user_name'] = user['full_name']
                    session['user_role'] = user['role']

                    # Redirect based on role: Admin or Student
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('student_dashboard'))
                else:
                    return "Invalid password. Try again."
            else:
                return "No user found with this email."

        except Exception as e:
            print(f"Login logic error: {e}")
            return "Internal Server Error."

    # This part handles the GET request (showing the page)
    return render_template('login.html')

# --- Other routes remain same ---
@app.route('/student/dashboard')
def student_dashboard():
    # Security: Only allow logged-in students
    if 'user_role' not in session or session['user_role'] != 'student':
        return redirect(url_for('login'))

    try:
        # Fetch resources along with subject names
        # Logic: select resource columns and the subject_name from the joined subjects table
        response = supabase.table("resources").select("*, subjects(subject_name, subject_code)").execute()
        all_resources = response.data
        
        print(f"DEBUG: Found {len(all_resources)} resources for students.")
    except Exception as e:
        print(f"Error fetching resources: {e}")
        all_resources = []

    return render_template('student/dashboard.html', resources=all_resources)

@app.route('/student/resources')
def student_resources():
   return render_template('student/resources.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

# Route to handle adding and viewing subjects (Admin only)
@app.route('/admin/manage-subjects', methods=['GET', 'POST'])
def manage_subjects():
    # Security: Check if user is logged in and is an admin
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('subject_name')
        code = request.form.get('subject_code')

        try:
            # Insert the new subject into Supabase
            supabase.table("subjects").insert({
                "subject_name": name,
                "subject_code": code
            }).execute()
            
            print(f"Subject {name} added successfully!")
            return redirect(url_for('manage_subjects'))
            
        except Exception as e:
            print(f"Error adding subject: {e}")
            return "Failed to add subject."

    # For GET request: Fetch all subjects to display in a table
    try:
        response = supabase.table("subjects").select("*").execute()
        subjects_list = response.data
    except Exception as e:
        print(f"Error fetching subjects: {e}")
        subjects_list = []

    return render_template('admin/manage_sub.html', subjects=subjects_list)

#Admin Upload Route
@app.route('/admin/upload', methods=['GET', 'POST'])
def upload_content():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        res_type = request.form.get('resource_type')
        subject_id = request.form.get('subject_id')
        file_url = request.form.get('file_url') # Manual link if provided
        
        # 1. Handle File Upload to Supabase Storage
        file = request.files.get('file_upload')
        
        if file and file.filename != '':
            try:
                # Create a unique filename using timestamp
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file_path = f"notes/{filename}"
                
                # Read file content
                file_content = file.read()
                
                # Upload to Supabase Storage Bucket 'study-material'
                storage_response = supabase.storage.from_("study-material").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": file.content_type}
                )
                
                # Get the Public URL of the uploaded file
                public_url_res = supabase.storage.from_("study-material").get_public_url(file_path)
                file_url = public_url_res # Use this URL for database
                
                print(f"File uploaded to storage: {file_url}")
                
            except Exception as storage_err:
                print(f"Storage Error: {storage_err}")
                return f"Failed to upload file to storage: {storage_err}"

        # 2. Insert into Database
        try:
            supabase.table("resources").insert({
                "title": title,
                "type": res_type,
                "subject_id": subject_id,
                "file_url": file_url
            }).execute()
            
            return redirect(url_for('admin_dashboard'))
        except Exception as db_err:
            print(f"Database Error: {db_err}")
            return f"Failed to save to database: {db_err}"

    # Fetch subjects for dropdown
    sub_response = supabase.table("subjects").select("*").execute()
    return render_template('admin/upload.html', subjects=sub_response.data)

# Logout Route to clear the session
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)