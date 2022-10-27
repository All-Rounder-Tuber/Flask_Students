from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

local_server = True

if local_server :
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Details(db.Model):
    roll = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    std = db.Column(db.String(10), nullable=True)
    sec = db.Column(db.String(5), nullable=True)
    father_name = db.Column(db.String(50), nullable=True)
    mother_name = db.Column(db.String(50), nullable=True)
    dob = db.Column(db.String(12), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    father_phone_num = db.Column(db.String(15), nullable=True)
    mother_phone_num = db.Column(db.String(15), nullable=True)


@app.route("/",  methods = ['GET','POST'])
def home():
    std_sec = request.form.get('std_sec')
    std_class = request.form.get('std_class')
    std_roll = request.form.get('std_roll')
    student = Details.query.filter_by(roll=std_roll, std=std_class, sec=std_sec).first()
    return render_template('home.html', params=params, student=student)

@app.route("/add", methods = ['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('std_name')
        std = request.form.get('std_class')
        roll = request.form.get('std_roll')
        sec = request.form.get('std_sec')
        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        address = request.form.get('address')
        dob = request.form.get('dob')
        father_phone_num = request.form.get('father_phone_num')
        mother_phone_num = request.form.get('mother_phone_num')

        entry = Details(roll=roll, name=name, std=std, sec=sec, father_name=father_name, mother_name=mother_name, dob=dob, address=address, father_phone_num=father_phone_num, mother_phone_num=mother_phone_num)
        db.session.add(entry)
        db.session.commit()
    

    return render_template('add.html', params=params)

@app.route("/update/<int:roll>", methods = ['GET', 'POST'])
def update(roll):
    if request.method == 'POST':
        name = request.form.get('std_name')
        std = request.form.get('std_class')
        roll = request.form.get('std_roll')
        sec = request.form.get('std_sec')
        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        address = request.form.get('address')
        dob = request.form.get('dob')
        father_phone_num = request.form.get('father_phone_num')
        mother_phone_num = request.form.get('mother_phone_num')

        student = Details.query.filter_by(roll=roll).first()

        student.name = name
        student.std = std
        student.roll = roll
        student.sec = sec
        student.father_name = father_name
        student.mother_name = mother_name
        student.address = address
        student.dob = dob
        student.father_phone_num = father_phone_num
        student.mother_phone_num = mother_phone_num

        db.session.add(student)
        db.session.commit()
        return redirect("/")

    student = Details.query.filter_by(roll=roll).first()
    return render_template('update.html', params=params, student = student)

@app.route("/delete/<int:roll>")
def delete(roll):
    student = Details.query.filter_by(roll=roll).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")

app.run(debug=True, host='0.0.0.0')