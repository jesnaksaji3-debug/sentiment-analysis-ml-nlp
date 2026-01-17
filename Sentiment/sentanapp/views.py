from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import datetime
from django.shortcuts import HttpResponseRedirect,redirect
from sentanapp.forms import UserForm
from sentanapp.models import User,Login
from django.http import HttpResponse
from django.db import connection
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, words
from nltk.stem import PorterStemmer
import nltk
import string
from textblob import TextBlob 

today_date = datetime.date.today()
today = today_date.strftime("%Y-%m-%d")
# Create your views here.
def index(request):
    return render(request,'index.html')
def user(request):
    return render(request,'user.html')
def adminhome(request):
    return render(request,'adminhome.html')
def userhome(request):
    return render(request,'userhome.html')
def review(request):
    return render(request,'review.html')
def useraction(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            #create a new user object and populate the fields from the form data
            profile = User()
            profile.name = request.POST["name"]
            profile.address = request.POST["address"]
            profile.email = request.POST["email"]
            profile.gender = request.POST["gender"]
            profile.contact = request.POST["contact"]
            profile.place = request.POST["place"]
            profile.district = request.POST["district"]
            profile.save() #save the new registration entry to db

            #fetch the maximum uid(the last inserted registration ID)
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(uid) FROM user")
            max_uid = cursor.fetchone()[0]

            #now insert into the login table with uid as max(uid)
            pro = Login()
            pro.uid = max_uid #Assign the fetched lid as uid
            pro.uname = request.POST["email"]
            pro.upass = request.POST["password"]
            pro.utype = 'User'
            pro.save()

            #Alet the user that the record was added and redirect to /index/
            msg="<script>alert('Added');window.location='/index/';</script>"
            return HttpResponse(msg)
    else:
        form = UserForm() #Render an empty from for GET requests

    return render(request, 'user.html', {'form': form}) #Render the form

def viewuser(request):
    #Fetch all records from the User table using Django's ORM
    users = User.objects.all()

    #Create a list of dictionaries with the user details
    usr = []
    for user in users:
        y = {
            'uid': user.uid,
            'name': user.name,
            'address': user.address,
            'email': user.email,
            'gender': user.gender,
            'contact': user.contact,
            'place': user.place,
            'district': user.district
        }
        usr.append(y)

    #pass the user list to the template
    return render(request, 'viewuser.html', {'usr': usr})
def login(request):
    return render(request,'login.html')
def loginaction(request):
    cursor=connection.cursor()
    un=request.GET['uname']
    up=request.GET['upass']
    s="select * from login where uname='%s' and upass='%s'"%(un,up)
    cursor.execute(s)
    print(s)
    if(cursor.rowcount)>0:
        rs=cursor.fetchall()
        for row in rs:
            request.session['uid']=row[1]
            request.session['uname']=row[2]
            request.session['upass']=row[3]
            request.session['utype']=row[4]
        if(request.session['utype']=='Admin'):
            return render(request,'adminhome.html')
        elif(request.session['utype']=='User'):
            return render(request,'userhome.html')
    else:
        msg="<script>alert('Login Failed');window.location='/login/';</script>"
        return HttpResponse(msg)

def deleteUser(request):
    cursor=connection.cursor()
    ids=request.GET['uid']
    s1="delete from user where uid='%s'"%(ids)
    cursor.execute(s1)
    s2="delete from login where uid='%s' and utype='User'"%(ids)
    cursor.execute(s2)
    msg="<script>alert('Successfully Deleted');window.location='/viewuser/';</script>"
    return HttpResponse(msg)


stop_words = set(stopwords.words('english'))
english_vocab = set(words.words())

def is_meaningful_review(text):
    if not text or len(text.strip()) < 10:
        return False

    tokens = word_tokenize(text)
    words_only = [w for w in tokens if w.isalpha()]

    if len(words_only) < 3:
        return False
    
    if not any(word.lower() in english_vocab for word in words_only):
        return False
    
    return True

def reviewact(request):
    if request.method == "POST":
        cursor = connection.cursor()
        pdtname = request.POST.get("pdtname")
        review = request.POST.get("review")
        uid = request.session.get("uid")

        if not is_meaningful_review(review):
            return HttpResponse("<script>alert('Please enter a meaningful review.'); window.location='/review/';</script>")

        blob = TextBlob(review)
        polarity = blob.sentiment.polarity

        if polarity >= 0.6:
            rating = 5
            sentiment = "Strongly Positive"
        elif polarity >= 0.3:
            rating = 4
            sentiment = "Positive"
        elif polarity >= -0.1:
            rating = 3
            sentiment = "Neutral"
        elif polarity >= -0.5:
            rating = 2
            sentiment = "Negative"
        else:
            rating = 1
            sentiment = "Strongly Negative"
        cursor.execute(
            "INSERT INTO review(pdtname, review, rating, uid) VALUES(%s, %s, %s, %s)",
            [pdtname, review, rating, uid]
        )
        connection.commit()

        return HttpResponse(f"<script>alert('Review submitted successfully with a {sentiment} sentiment.'); window.location='/review/';</script>")
    
    return HttpResponse("<script>alert('Invalid request'); window.location='/review/';</script>")