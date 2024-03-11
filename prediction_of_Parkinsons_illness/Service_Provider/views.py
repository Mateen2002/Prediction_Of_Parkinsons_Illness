
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, matthews_corrcoef
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_parkinsons_illness,detection_ratio,detection_accuracy


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def Find_View_Prediction_DDOS_Attack_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    ratio = ""
    kword = 'Found'
    print(kword)
    obj = predict_parkinsons_illness.objects.all().filter(Q(Prediction=kword))
    obj1 =predict_parkinsons_illness.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Not Found'
    print(kword1)
    obj1 = predict_parkinsons_illness.objects.all().filter(Q(Prediction=kword1))
    obj11 = predict_parkinsons_illness.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)

    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/Find_View_Prediction_DDOS_Attack_Type_Ratio.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = predict_parkinsons_illness.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_DDOS_Attack_Type(request):
    obj =predict_parkinsons_illness.objects.all()
    return render(request, 'SProvider/View_Prediction_DDOS_Attack_Type.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="PredictedData.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = predict_parkinsons_illness.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.RID, font_style)
        ws.write(row_num, 1, my_row.name, font_style)
        ws.write(row_num, 2, my_row.MDVP_Fo_Hz, font_style)
        ws.write(row_num, 3, my_row.MDVP_Fhi_Hz, font_style)
        ws.write(row_num, 4, my_row.MDVP_Flo_Hz, font_style)
        ws.write(row_num, 5, my_row.MDVP_Jitter, font_style)
        ws.write(row_num, 6, my_row.MDVP_Jitter_Abs, font_style)
        ws.write(row_num, 7, my_row.MDVP_RAP, font_style)
        ws.write(row_num, 8, my_row.MDVP_PPQ, font_style)
        ws.write(row_num, 9, my_row.Jitter_DDP, font_style)
        ws.write(row_num, 10, my_row.MDVP_Shimmer, font_style)
        ws.write(row_num, 11, my_row.MDVP_Shimmer_dB, font_style)
        ws.write(row_num, 12, my_row.Shimmer_APQ3, font_style)
        ws.write(row_num, 13, my_row.Shimmer_APQ5, font_style)
        ws.write(row_num, 14, my_row.MDVP_APQ, font_style)
        ws.write(row_num, 15, my_row.Shimmer_DDA, font_style)
        ws.write(row_num, 16, my_row.NHR, font_style)
        ws.write(row_num, 17, my_row.HNR, font_style)
        ws.write(row_num, 18, my_row.RPDE, font_style)
        ws.write(row_num, 19, my_row.DFA, font_style)
        ws.write(row_num, 20, my_row.spread1, font_style)
        ws.write(row_num, 21, my_row.spread2, font_style)
        ws.write(row_num, 22, my_row.D2, font_style)
        ws.write(row_num, 23, my_row.PPE, font_style)
        ws.write(row_num, 24, my_row.Prediction, font_style)



    wb.save(response)
    return response

def Train_Test_DataSets(request):
    detection_accuracy.objects.all().delete()

    df = pd.read_csv('Datasets.csv',encoding='latin-1')
    df
    df.columns

    def apply_response(Label):
        if (Label == 0):
            return 0  # Not Found
        elif (Label == 1):
            return 1  # Found

    df['Results'] = df['status'].apply(apply_response)

    X = df['RID'].apply(str)
    y = df['Results']

    X.shape, y.shape


    print("Reading ID")
    print(X)
    print("Label")
    print(y)

    cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
    X = cv.fit_transform(df['RID'].apply(lambda x: np.str_(x)))
    #cv = CountVectorizer()
    #X = cv.fit_transform(X)

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
    detection_accuracy.objects.create(names="Naive Bayes", ratio=naivebayes)

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
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)


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

    detection_accuracy.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred) * 100)


    print("Random Forest Classifier")
    from sklearn.ensemble import RandomForestClassifier
    rf_clf = RandomForestClassifier()
    rf_clf.fit(X_train, y_train)
    rfpredict = rf_clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, rfpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, rfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, rfpredict))
    models.append(('RandomForestClassifier', rf_clf))
    detection_accuracy.objects.create(names="Random Forest Classifier", ratio=accuracy_score(y_test, rfpredict) * 100)


    predicts = 'predicts.csv'
    df.to_csv(predicts, index=False)
    df.to_markdown

    obj = detection_accuracy.objects.all()


    return render(request,'SProvider/Train_Test_DataSets.html', {'objs': obj})