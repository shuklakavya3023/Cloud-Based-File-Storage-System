import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from dotenv import load_dotenv
import boto3
from authlib.integrations.flask_client import OAuth
from io import BytesIO

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cloud-drive-secret-123")

# AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION", "ap-south-1")
)
BUCKET = os.getenv("S3_BUCKET")

# Google OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['user'] = user_info
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    resp = s3.list_objects_v2(Bucket=BUCKET)
    files = [obj['Key'] for obj in resp.get('Contents', [])]
    return render_template('dashboard.html', user=session['user'], files=files)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f:
        s3.upload_fileobj(f, BUCKET, f.filename)
    return redirect('/dashboard')

@app.route('/download/<filename>')
def download_file(filename):
    bio = BytesIO()
    s3.download_fileobj(BUCKET, filename, bio)
    bio.seek(0)
    return send_file(bio, download_name=filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    s3.delete_object(Bucket=BUCKET, Key=filename)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)