from flask import Flask, render_template, redirect
from flask.globals import request
from form import ShortenURL
from pymongo import MongoClient
import random
from functions import url_check
import string

db = MongoClient('mongodb+srv://NeilShah:RBQsucAwtKMCtrgi@cluster0.e5qrs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = db["projects"]
db_url = db["url"]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Neil'


@app.route('/', methods=('GET', 'POST'))
def index():
    form = ShortenURL(request.form)

    if request.method == 'POST':

        if form.validate():
            url = request.form.get('url')
            
            number = random.randint(100, 999)
            number = str(number)
            number2 = random.randint(1, 9)
            number2 = str(number2)
            letter2 = random.choice(string.ascii_uppercase)
            letter = random.choice(string.ascii_lowercase)
            number = number + letter + number2 + letter2
            count = db_url.count_documents({})
            post = {"_id": count + 1, "url": url, "extention": number, "used": 0}
            db_url.insert_one(post)
            return f"""<h1>Your Link: localhost:5000/{number}"""            

        elif form.validate() == False:
            print("Invalid")

    return render_template('index.html', form=form)

@app.route('/<ext>')
def route(ext):

    try:    
        search = db_url.find({"extention": ext})

        for i in search:
            url = i['url']
            count = i['used']

        db_url.update_one({"extention": ext}, {"$set": {"used": count + 1}})

        new_url = url_check(url)
        return redirect(new_url)
    

    except UnboundLocalError:
        return f"""<h1>Please Enter A Valid Extention</h1>"""

@app.route('/track/<code>')
def track(code):
    search = db_url.find({"extention": code})
    for i in search:
        count = i['used']
    return render_template('count.html', count=count)
