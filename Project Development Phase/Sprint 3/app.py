from flask import Flask,request,redirect,url_for,flash,render_template
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user
from forms import *
import numpy as np
import pickle
import json
import requests

app=Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
app.secret_key='Secret key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database2.sqlite3'
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

from model import *

login_manager=LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup',methods=['POST'])
def register():
    from model import user
    email=request.form.get('email')
    username=request.form.get('username')
    password=request.form.get('password')

    User=user.query.filter_by(username=username).first()
    if User:
        flash('Username Already exists')
        return redirect(url_for('signup'))
    
    new_user=user(username=username, email=email, password=generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def logging_in():
    username=request.form.get('username')
    password=request.form.get('password')
    remember= True if request.form.get('Remember user') else False

    User=user.query.filter_by(username=username).first()

    if User and check_password_hash(User.password, password):
        login_user(User)
        return redirect(url_for('dashboard',current_id=User.id))
    else:   
        flash('Please Check your credentials and try again')
        return redirect(url_for('login'))

@app.route('/dashboard/<int:current_id>')
@login_required
def dashboard(current_id):
    students=student.query.filter_by(user_id=current_id)
    return render_template('dashboard.html', collections=students, name=current_user.username)

@app.route('/add_profile',methods=['GET','POST'])
def add_profile():
    form=profileform()
    if form.validate_on_submit():
        students=student(name=form.name.data, place=form.place.data, number=form.number.data, occupation=form.occupation.data)
        value=current_user.id
        students.user_id=value
        db.session.add(students)
        db.session.commit()
        return redirect(url_for('dashboard',current_id=value))
    return render_template('add_profile.html', form=form)

@app.route('/edit_profile/<int:student_id>',methods=['GET','POST'])
def edit_profile(student_id):
    form=Editprofileform()
    studente=student.query.filter_by(id=student_id).first()
    if form.validate_on_submit():
        studente.name=form.name.data
        studente.place=form.place.data
        studente.number=form.number.data
        studente.occupation=form.occupation.data
        db.session.add(studente)
        db.session.commit()
        return redirect(url_for('dashboard',current_id=current_user.id))
    return render_template('edit_profile.html', form=form)


@app.route('/delete_profile/<int:student_id>')
def delete_deck(student_id):
    studente=student.query.filter_by(id=student_id).first()
    db.session.delete(studente)
    db.session.commit()
    return redirect(url_for('dashboard', current_id=current_user.id))

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        float_features=[float(x) for x in request.form.values()]
        final_features=[np.array(float_features)]
        prediction=model.predict(final_features)

        value=round(prediction[0]*100,2)
        if value>70:
            return render_template('predict.html', pred='High chance of admission.\nChance of admit is {} percent'.format(value))
        else:
            return render_template('predict.html', pred='Low chance of admission.\nChance of admit is {} percent'.format(value))
    else:
        return render_template('predict.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)


