from ast import alias
from concurrent.futures import process
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages

import Spam_Detection_In_Short_Message_Service

from .forms import UserRegistrationForm
from .models import UserRegistrationModel, UserActivityLog, PredictionReport
from django.conf import settings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import datetime as dt
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import re

# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # -----------------------------
        # VALIDATIONS
        # -----------------------------

        # 1. Mobile validation (Indian)
        if not re.match(r'^[6-9][0-9]{9}$', mobile):
            messages.error(request, "Invalid mobile number. Must be 10 digits and start with 6-9.")
            return render(request, 'UserRegistrations.html')

        # 2. Password validation
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password):
            messages.error(request, "Password must have 1 capital letter, 1 number, 1 special symbol, and be at least 8 characters long.")
            return render(request, 'UserRegistrations.html')

        # 3. Check duplicate login ID
        if UserRegistrationModel.objects.filter(loginid=loginid).exists():
            messages.error(request, "Login ID already taken. Try another.")
            return render(request, 'UserRegistrations.html')

        # 4. Check duplicate mobile
        if UserRegistrationModel.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already registered.")
            return render(request, 'UserRegistrations.html')

        # 5. Check duplicate email
        if UserRegistrationModel.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'UserRegistrations.html')

        # -----------------------------
        # SAVE DATA
        # -----------------------------
        UserRegistrationModel.objects.create(
            name=name,
            loginid=loginid,
            password=password,
            mobile=mobile,
            email=email,
            locality=locality,
            address=address,
            city=city,
            state=state,
            status='waiting'
        )

        messages.success(request, "Registration successful!")
        return render(request, 'UserRegistrations.html')

    return render(request, 'UserRegistrations.html')

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                log = UserActivityLog.objects.create(user_loginid=loginid, user_role=check.role)
                request.session['log_id'] = log.id
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

def UserReportView(request):
    uid = request.session.get('loginid', '')
    data = PredictionReport.objects.filter(user_loginid=uid).order_by('-created_at')
    return render(request, 'users/UserReport.html', {'data': data})

def DatasetView(request):
    from django.conf import settings
    path = settings.MEDIA_ROOT + "//" + 'balanced_spam_dataset.csv'
    df = pd.read_csv(path)
    df = df.to_html
    return render(request, 'users/viewdataset.html', {'data': df})

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
path = settings.MEDIA_ROOT + "//" + 'balanced_spam_dataset.csv'
df = pd.read_csv(path)
value_counts = df['Category'].value_counts()
# print(value_counts)
# import matplotlib.pyplot as plt
# # Plotting the bar plot
# value_counts.plot(kind='bar')
# # Adding labels and title
# plt.xlabel('Categories')
# plt.ylabel('Counts')
# plt.title('Value Counts of Your Column')
# # Displaying the plot
# plt.show()
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['Message'], df['Category'], test_size=0.2, random_state=42)
# Vectorize the tweets using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=10000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)
# Train a Naive Bayes classifier
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_tfidf, y_train)

# Train Support Vector Machine (SVM)
svm_classifier = SVC(kernel='linear', probability=True)
svm_classifier.fit(X_train_tfidf, y_train)

# Train Logistic Regression
lr_classifier = LogisticRegression(max_iter=1000)
lr_classifier.fit(X_train_tfidf, y_train)

# Train Random Forest
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_tfidf, y_train)

# Train K-Means
kmeans_model = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans_model.fit(X_train_tfidf)


def machine_learning(request):  
    # Predicting Accuracies
    # Naive Bayes
    nb_preds = nb_classifier.predict(X_test_tfidf)
    nb_acc = accuracy_score(y_test, nb_preds)
    
    # SVM
    svm_preds = svm_classifier.predict(X_test_tfidf)
    svm_acc = accuracy_score(y_test, svm_preds)
    
    # Logistic Regression
    lr_preds = lr_classifier.predict(X_test_tfidf)
    lr_acc = accuracy_score(y_test, lr_preds)
    
    # Random Forest
    rf_preds = rf_classifier.predict(X_test_tfidf)
    rf_acc = accuracy_score(y_test, rf_preds)
    
    # K-Means mapping
    kmeans_preds = kmeans_model.predict(X_test_tfidf)
    # Check mapping
    import numpy as np
    classes = y_test.unique()
    if len(classes) == 2:
        class_0, class_1 = classes[0], classes[1]
        kmeans_preds_mapped_1 = np.where(kmeans_preds == 0, class_0, class_1)
        kmeans_acc_1 = accuracy_score(y_test, kmeans_preds_mapped_1)
        kmeans_preds_mapped_2 = np.where(kmeans_preds == 0, class_1, class_0)
        kmeans_acc_2 = accuracy_score(y_test, kmeans_preds_mapped_2)
        kmeans_acc = max(kmeans_acc_1, kmeans_acc_2)
    else:
        kmeans_acc = 0
    
    context = {
        'nb_acc': round(nb_acc * 100, 2),
        'svm_acc': round(svm_acc * 100, 2),
        'lr_acc': round(lr_acc * 100, 2),
        'rf_acc': round(rf_acc * 100, 2),
        'kmeans_acc': round(kmeans_acc * 100, 2),
        # Legacy variable 'acc' to not break existing templates blindly
        'acc': round(nb_acc * 100, 2),
        'recent_preds': PredictionReport.objects.all().order_by('-created_at')[:50],
    }
    return render(request, "users/machine_learning.html", context)

'''
a classification label, with possible values including 
spam (0), Not Spam (1).
'''


def prediction(request):
    if request.method == 'POST':
        single_tweet = request.POST.get('tweets', '') 
        screenshot = request.FILES.get('screenshot')
        camera_data = request.POST.get('camera_data')
        
        extracted_text = ""
        ocr_images = []
        
        if screenshot:
            ocr_images.append(screenshot)
            
        if camera_data and camera_data.startswith('data:image'):
            try:
                import base64
                from io import BytesIO
                format, imgstr = camera_data.split(';base64,') 
                decoded_img = base64.b64decode(imgstr)
                camera_file = BytesIO(decoded_img)
                ocr_images.append(camera_file)
            except Exception as e:
                print("Error decoding camera data:", str(e))

        if ocr_images:
            import pytesseract
            import os
            from PIL import Image
            
            # Configure Tesseract path for Windows (local) vs Linux (Railway)
            if os.name == 'nt':
                # Local Windows path where Tesseract will be installed
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # (On Railway Linux, the default system PATH works out-of-the-box!)
                
            all_extracted = []
            for img_source in ocr_images:
                try:
                    img = Image.open(img_source).convert('RGB')
                    text = pytesseract.image_to_string(img)
                    if text.strip():
                        all_extracted.append(text.strip())
                except Exception as e:
                    print(f"Error OCR: {str(e)}")
            
            if all_extracted:
                extracted_text = " ".join(all_extracted)
                
        # Combine extracted text with the typed text
        combined_text = (single_tweet + " " + extracted_text).strip()
        
        # Pre-process: Extract Behavioral Signals and Clean Text
        input_text_raw = combined_text
        behavioral_risk = 'LOW'
        if '[Behavioral Risk Output: HIGH]' in input_text_raw:
            behavioral_risk = 'HIGH'
        elif '[Behavioral Risk Output: MEDIUM]' in input_text_raw:
            behavioral_risk = 'MEDIUM'
            
        # Clean text for ML models (strip our prefixes)
        import re
        clean_text = re.sub(r'\[Behavioral Risk Output:.*?\]', '', input_text_raw)
        clean_text = re.sub(r'Signals: Reading=.*?\n', '', clean_text)
        clean_text = clean_text.strip()
        
        if not clean_text and not extracted_text:
            return render(request, 'users/predictForm.html', {'output': 'Please enter text or upload an image.'})

        # Make prediction
        pred_type = request.POST.get('pred_type', 'single')
        algos_to_use = []
        if pred_type == 'single':
            algos_to_use.append(request.POST.get('single_algo', 'nb'))
        else:
            algos_to_use = request.POST.getlist('hybrid_algos') or ['nb']

        single_tweet_tfidf = tfidf_vectorizer.transform([clean_text])
        
        results = []
        for algo in algos_to_use:
            if algo == 'nb':
                pred = nb_classifier.predict(single_tweet_tfidf)[0]
            elif algo == 'svm':
                pred = svm_classifier.predict(single_tweet_tfidf)[0]
            elif algo == 'lr':
                pred = lr_classifier.predict(single_tweet_tfidf)[0]
            elif algo == 'rf':
                pred = rf_classifier.predict(single_tweet_tfidf)[0]
            elif algo == 'kmeans':
                pred_raw = kmeans_model.predict(single_tweet_tfidf)[0]
                known_spam = tfidf_vectorizer.transform(["win free money prize claim urgent viagra lottery winner"])
                spam_cluster = kmeans_model.predict(known_spam)[0]
                pred = 'spam' if pred_raw == spam_cluster else 'non-spam'
            else:
                pred = 'non-spam'
                
            pred_str = str(pred).lower().strip()
            results.append('spam' if pred_str in ['0', 'spam'] else 'non-spam')

        spam_count = results.count('spam')
        non_spam_count = results.count('non-spam')
        
        # FUSION LOGIC: Behavioral Risk + ML Votes + Keyword Penalty
        final_prediction = 'non-spam'
        CRITICAL_MARKERS = ['otp', 'account blocked', 'verify your identity', 'unauthorized login', 'winner of', 'cash prize']
        has_critical = any(marker in clean_text.lower() for marker in CRITICAL_MARKERS)
        
        if behavioral_risk == 'HIGH':
            final_prediction = 'spam'
        elif has_critical and (spam_count > 0 or behavioral_risk == 'MEDIUM'):
            final_prediction = 'spam'
        elif spam_count > non_spam_count:
            final_prediction = 'spam'
        
        algo_names = {'nb': 'Naive Bayes', 'svm': 'SVM', 'lr': 'Logistic Regression', 'rf': 'Random Forest', 'kmeans': 'K-Means'}
        applied_str = ", ".join([algo_names.get(a, a) for a in algos_to_use])
        record_name = f'Hybrid ({applied_str})' if pred_type == 'hybrid' else applied_str

        # Determine input type for reporting
        input_type = request.POST.get('input_source', 'text')
        if screenshot: input_type = 'image'
            
        PredictionReport.objects.create(
            user_loginid=request.session.get('loginid', 'Anonymous'), 
            algorithm_name=record_name, 
            input_text=input_text_raw[:2000], 
            input_type=input_type,
            prediction_result=final_prediction
        )
        return render(request, 'users/predictForm.html', {'output':final_prediction, 'extracted_text': extracted_text})
    return render(request, 'users/predictForm.html', {})
