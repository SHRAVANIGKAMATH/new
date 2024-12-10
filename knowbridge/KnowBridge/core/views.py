from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .firebase_config import db
from firebase_admin import auth as firebase_auth, exceptions, firestore
import bcrypt
import easyocr
from PIL import Image
import io
import logging
import pytz  # Ensure pytz is imported
from groq import Groq
from django.shortcuts import render
import warnings

warnings.filterwarnings(
    "ignore",
    message="Detected filter using positional arguments.*",
    category=UserWarning,
    module="google.cloud.firestore_v1.base_collection",
)

syllabus_text=''

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def get_started(request):
    return render(request, 'get_started.html')

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            identifier = form.cleaned_data.get('identifier').lower()
            user_type = form.cleaned_data.get('user_type')

            existing_user = db.collection('users').where(field_path='identifier', op_string='==', value=identifier).get()

            if len(existing_user) > 0:
                messages.error(request, "Identifier already exists. Please choose a different identifier.")
                return render(request, 'register.html', {'form': form})

            try:
                user = firebase_auth.create_user(email=email, password=password)
                user_data = {
                    'username': username,
                    'email': email,
                    'identifier': identifier,
                    'hashed_password': hashed_password,  # Storing hashed password
                    'is_teacher': user_type == 'teacher',
                    'is_student': user_type == 'student'
                }
                db.collection('users').document(user.uid).set(user_data)
                print(f"Stored user data: {user_data}")  # Debug print

                request.session['uid'] = user.uid

                if user_type == 'teacher':
                    messages.success(request, "Registration successful! Redirecting to Teacher Dashboard.")
                    return redirect('teacher_dashboard')
                else:
                    messages.success(request, "Registration successful! Redirecting to Student Dashboard.")
                    return redirect('student_dashboard')

            except firebase_auth.EmailAlreadyExistsError:
                messages.error(request, "Email already in use. Please use a different email.")
            except Exception as e:
                logger.error(f"Registration failed: {e}")
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            messages.error(request, "Invalid form submission. Please correct the errors and try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def role_selection(request):
    return render(request, 'role_selection.html')

import warnings

# Suppress the UserWarning from Firestore
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning, module='google.cloud.firestore_v1.base_collection')

# The rest of your imports

import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect
from google.cloud import firestore
from google.oauth2 import service_account

# Initialize Firestore with credentials
credentials = service_account.Credentials.from_service_account_file(
    'C:\\Users\\kshra\\knowbridge\\knowbridge\\education-49071-firebase-adminsdk-rer49-e12e4b2c29.json')
db = firestore.Client(credentials=credentials)

def login_teacher(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier').lower()
            password = form.cleaned_data.get('password')
            try:
                user_docs = db.collection('users').where('identifier', '==', identifier).stream()
                user_doc_list = list(user_docs)
                if not user_doc_list:
                    messages.error(request, "Enter a valid identifier.")
                else:
                    user_data = user_doc_list[0].to_dict()
                    if 'hashed_password' not in user_data:
                        messages.error(request, "Login failed! Please check your credentials and try again.")
                        return render(request, 'login_teacher.html', {'form': form})
                    if bcrypt.checkpw(password.encode('utf-8'), user_data['hashed_password'].encode('utf-8')):
                        if user_data.get('is_teacher'):
                            request.session['uid'] = user_doc_list[0].id
                            messages.success(request, "Login successful! Redirecting to Teacher Dashboard.")
                            return redirect('teacher_dashboard')
                        else:
                            messages.error(request, "You are not registered as a teacher.")
                    else:
                        messages.error(request, "Incorrect credentials. Please try again.")
            except Exception as e:
                logger.error(f"Login failed: {e}")
                messages.error(request, f"Login failed! Please check your credentials and try again. {str(e)}")
    else:
        form = CustomUserLoginForm()
    return render(request, 'login_teacher.html', {'form': form})

def login_student(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier').lower()
            password = form.cleaned_data.get('password')
            try:
                user_docs = db.collection('users').where('identifier', '==', identifier).stream()
                user_doc_list = list(user_docs)
                if not user_doc_list:
                    messages.error(request, "Enter a valid identifier.")
                else:
                    user_data = user_doc_list[0].to_dict()
                    if 'hashed_password' not in user_data:
                        messages.error(request, "Login failed! Please check your credentials and try again.")
                        return render(request, 'login_student.html', {'form': form})
                    if bcrypt.checkpw(password.encode('utf-8'), user_data['hashed_password'].encode('utf-8')):
                        if user_data.get('is_student'):
                            request.session['uid'] = user_doc_list[0].id
                            messages.success(request, "Login successful! Redirecting to Student Dashboard.")
                            return redirect('student_dashboard')
                        else:
                            messages.error(request, "You are not registered as a student.")
                    else:
                        messages.error(request, "Incorrect credentials. Please try again.")
            except Exception as e:
                logger.error(f"Login failed: {e}")
                messages.error(request, f"Login failed! Please check your credentials and try again. {str(e)}")
    else:
        form = CustomUserLoginForm()
    return render(request, 'login_student.html', {'form': form})


from datetime import datetime

logger = logging.getLogger(__name__)

import easyocr
from PIL import Image
import io
from django.shortcuts import render, redirect
from django.contrib import messages
import logging
import firebase_admin
from firebase_admin import firestore
import pytz
from datetime import datetime
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser
import bcrypt  # Ensure bcrypt is imported

# Initialize Firebase app
if not firebase_admin._apps:
    firebase_admin.initialize_app()

logger = logging.getLogger(__name__)

from django.http import JsonResponse  # If you want to return JSON responses for MCQs
import os
from groq import Groq
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
import pytz
import easyocr
from PIL import Image
import io

os.environ['GROQ_API_KEY'] = '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'

import os
import io
from datetime import datetime
from PIL import Image
import pytz
import easyocr
from groq import Groq
from django.contrib import messages
from django.shortcuts import render

os.environ['GROQ_API_KEY'] = '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'

def generate_mcqs(topic, num_questions):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Generate {num_questions} multiple-choice questions about {topic}, each with four options and the correct answer marked. Make sure questions are not too easy or too tough."},
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

def teacher_dashboard(request):
    user_id = request.session.get('uid')
    syllabus_text = ""
    chapters = []
    mcqs = {}

    # Fetch syllabus and chapters from the database
    if user_id:
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            syllabus_entries = user_data.get('syllabus_text', [])
            syllabus_entries = [entry for entry in syllabus_entries if isinstance(entry, dict)]
            
            if syllabus_entries:
                latest_entry = max(syllabus_entries, key=lambda x: x.get('timestamp'))
                if isinstance(latest_entry, dict):
                    syllabus_text = latest_entry.get('text', "")
                    chapters = latest_entry.get('chapters', [])

    # Process uploaded syllabus file
    if request.method == 'POST':
        file = request.FILES.get('syllabus_file')
        if file:
            try:
                file_bytes = file.read()
                reader = easyocr.Reader(['en'], gpu=False)
                image = Image.open(io.BytesIO(file_bytes))
                image_bytes = io.BytesIO()
                image.save(image_bytes, format=image.format)
                image_bytes = image_bytes.getvalue()

                result = reader.readtext(image_bytes, detail=0, paragraph=True)
                parsed_text = ' '.join(result)
                chapters = [chapter.strip() for part in parsed_text.split('.') for chapter in part.split(',') if chapter.strip()]

                if user_id:
                    ist = pytz.timezone('Asia/Kolkata')
                    current_time = datetime.now(ist).astimezone(ist)
                    ocr_data = {
                        'user_id': user_id,
                        'syllabus_text': parsed_text,
                        'chapters': chapters,
                        'flagged': False,
                        'timestamp': current_time
                    }
                    db.collection('ocr_results').add(ocr_data)
                    db.collection('users').document(user_id).update({
                        'syllabus_text': firestore.ArrayUnion([{
                            'text': parsed_text,
                            'chapters': chapters,
                            'timestamp': current_time
                        }])
                    })

                    syllabus_text = parsed_text
                    messages.success(request, "OCR Successful! Parsed text and chapters stored.")
                else:
                    messages.error(request, "User session expired. Please log in again.")
            except Exception as e:
                messages.error(request, f"Failed to process file: {str(e)}")
        else:
            messages.error(request, "No file uploaded. Please upload a syllabus file.")

    # Generate MCQs for each chapter
    if chapters:
        try:
            for chapter in chapters:
                raw_mcqs = generate_mcqs(chapter, num_questions=5)
                mcqs[chapter] = raw_mcqs.split("\n")  # Split MCQs into a list
        except Exception as e:
            messages.error(request, f"Failed to generate MCQs: {str(e)}")

    return render(request, 'teacher_dashboard.html', {
        'syllabus_text': syllabus_text,
        'chapters': chapters,
        'mcqs': mcqs
    })


from django.shortcuts import render
import random


def generate_mcq_tests(request):
    print("In generate_mcq_tests")
    if request.method == 'POST':
        print("POST request received")  # Debugging print statement
        user_id = request.session.get('uid')
        user_doc = db.collection('users').document(user_id).get()

        # Fetch all chapters from 'ocr_results'
        ocr_results = db.collection('ocr_results').stream()
        chapters = []
        for doc in ocr_results:
            data = doc.to_dict()
            if 'chapters' in data:
                chapters.extend(data['chapters'])

        # Ensure chapters are unique
        chapters = list(set(chapters))
        print(f"Extracted chapters: {chapters}")  # Debugging print

        if not chapters:
            messages.error(request, "No chapters found to generate MCQs.")
            return redirect('generate_mcq_tests')

        # Choose a random chapter to generate MCQs
        selected_chapter = random.choice(chapters)
        print(f"Selected chapter: {selected_chapter}")  # Debugging print

        # Set number of questions to generate
        num_questions = 5

        # Generate MCQs
        mcq_tests = generate_mcqs(selected_chapter, num_questions)

        # Save MCQ tests in session for later access
        request.session['mcq_tests'] = mcq_tests
        print(f"Generated MCQs: {mcq_tests}")  # Debugging print

        return render(request, 'mcq_tests.html', {'mcq_tests': mcq_tests})

    return render(request, 'generate_mcq_tests.html')


def confirm_mcq_tests(request):
    if request.method == 'POST':
        mcq_tests = request.session.get('mcq_tests', [])
        user_id = request.session.get('uid')
        
        if user_id and mcq_tests:
            db.collection('users').document(user_id).update({
                'mcq_tests': firestore.ArrayUnion(mcq_tests)
            })
            messages.success(request, "MCQ tests confirmed and sent to students.")
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Failed to confirm MCQ tests.")
            return redirect('generate_mcq_tests')
    return redirect('teacher_dashboard')

def student_dashboard(request):
    user_id = request.session.get('uid')
    latest_syllabus_text = ""
    chapters = []
    mcq_tests = []

    if user_id:
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            syllabus_entries = user_data.get('syllabus_text', [])

            # Ensure syllabus_entries is a list of dictionaries
            syllabus_entries = [entry for entry in syllabus_entries if isinstance(entry, dict)]
            
            if syllabus_entries:
                latest_entry = max(syllabus_entries, key=lambda x: x.get('timestamp'))
                if isinstance(latest_entry, dict):  # Ensure latest_entry is a dictionary
                    latest_syllabus_text = latest_entry.get('text', "")
                    chapters = latest_entry.get('chapters', [])
                    
            mcq_tests = user_data.get('mcq_tests', [])

    return render(request, 'student_dashboard.html', {
        'user_data': user_data,
        'syllabus_text': latest_syllabus_text,
        'chapters': chapters,
        'mcq_tests': mcq_tests
    })

def user_logout(request):
    logout(request)
    return redirect('home')
def hello(request):
    return render(request, 'hello.html')
def contact(request):
    return render(request, 'contact.html')