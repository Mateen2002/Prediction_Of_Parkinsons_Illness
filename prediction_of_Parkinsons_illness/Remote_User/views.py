from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore")
plt.style.use('ggplot')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_parkinsons_illness,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def predict_ddos_attack_type(request):
    if request.method == "POST":

        RID= request.POST.get('RID')
        name= request.POST.get('name')
        MDVP_Fo_Hz= request.POST.get('MDVP_Fo_Hz')
        MDVP_Fhi_Hz= request.POST.get('MDVP_Fhi_Hz')
        MDVP_Flo_Hz= request.POST.get('MDVP_Flo_Hz')
        MDVP_Jitter= request.POST.get('MDVP_Jitter')
        MDVP_Jitter_Abs= request.POST.get('MDVP_Jitter_Abs')
        MDVP_RAP= request.POST.get('MDVP_RAP')
        MDVP_PPQ= request.POST.get('MDVP_PPQ')
        Jitter_DDP= request.POST.get('Jitter_DDP')
        MDVP_Shimmer= request.POST.get('MDVP_Shimmer')
        MDVP_Shimmer_dB= request.POST.get('MDVP_Shimmer_dB')
        Shimmer_APQ3= request.POST.get('Shimmer_APQ3')
        Shimmer_APQ5= request.POST.get('Shimmer_APQ5')
        MDVP_APQ= request.POST.get('MDVP_APQ')
        Shimmer_DDA= request.POST.get('Shimmer_DDA')
        NHR= request.POST.get('NHR')
        HNR= request.POST.get('HNR')
        RPDE= request.POST.get('RPDE')
        DFA= request.POST.get('DFA')
        spread1= request.POST.get('spread1')
        spread2= request.POST.get('spread2')
        D2= request.POST.get('D2')
        PPE= request.POST.get('PPE')




        df = pd.read_csv('Datasets.csv', encoding='latin-1')
        df
        df.columns

        def apply_response(Label):
            if (Label == 0):
                return 0  # Not Found
            elif (Label == 1):
                return 1  # Found

        df['Results'] = df['status'].apply(apply_response)

        X = df['RID']
        y = df['Results']

        print("Reading ID")
        print(X)
        print("Label")
        print(y)

        # cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
        # X = cv.fit_transform(df['RID'].apply(lambda x: np.str_(x)))
        cv = CountVectorizer()
        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB
        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print(naivebayes)
        print(confusion_matrix(y_test, predict_nb))
        print(classification_report(y_test, predict_nb))
        models.append(('naive_bayes', NB))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))



        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        RID1 = [RID]
        vector1 = cv.transform(RID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Not Found'
        elif prediction == 1:
            val = 'Found'



        print(val)
        print(pred1)

        predict_parkinsons_illness.objects.create(
        RID=RID,
        name=name,
        MDVP_Fo_Hz=MDVP_Fo_Hz,
        MDVP_Fhi_Hz=MDVP_Fhi_Hz,
        MDVP_Flo_Hz=MDVP_Flo_Hz,
        MDVP_Jitter=MDVP_Jitter,
        MDVP_Jitter_Abs=MDVP_Jitter_Abs,
        MDVP_RAP=MDVP_RAP,
        MDVP_PPQ=MDVP_PPQ,
        Jitter_DDP=Jitter_DDP,
        MDVP_Shimmer=MDVP_Shimmer,
        MDVP_Shimmer_dB=MDVP_Shimmer_dB,
        Shimmer_APQ3=Shimmer_APQ3,
        Shimmer_APQ5=Shimmer_APQ5,
        MDVP_APQ=MDVP_APQ,
        Shimmer_DDA=Shimmer_DDA,
        NHR=NHR,
        HNR=HNR,
        RPDE=RPDE,
        DFA=DFA,
        spread1=spread1,
        spread2=spread2,
        D2=D2,
        PPE=PPE,
       Prediction=val)

        return render(request, 'RUser/predict_ddos_attack_type.html',{'objs': val})
    return render(request, 'RUser/predict_ddos_attack_type.html')



