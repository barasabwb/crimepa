from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

 
# Settings for migrations
import pickle
import numpy as np
model = pickle.load(open('rf_model.pkl', 'rb'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

migrate = Migrate(app, db)
class Profile(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), unique=False, nullable=False)
    phone = db.Column(db.String(15), unique=False, nullable=False)
    incident_description = db.Column(db.String(1000), unique=False, nullable=False)
    crime_category = db.Column(db.String(100), unique=False, nullable=False)
    location = db.Column(db.String(100), unique=False, nullable=False)
    suspect_info = db.Column(db.String(1000), unique=False, nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)
    officer_in_charge = db.Column(db.String(100), unique=False, nullable=False)
    
 
    
    def __repr__(self):
        return f"Name : {self.full_name}, Age: {self.age}, Gender: {self.age}, Phone: {self.phone}, Incident Description: {self.incident_description}, Crime:{self.crime_category}, Location:{self.location}, Suspect_info:{self.suspect_info}, Date/Time:{self.date_and_time}, Officer:{self.officer_in_charge}"


@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('index.html')

@app.route('/make_prediction', methods=['GET', 'POST'])
def prediction_form():
   return render_template('prediction_form.html')
   
@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
   return render_template('heatmap.html')

@app.route('/visualizations')
def visualization():
   return render_template('visualizations.html')

@app.route('/report_crime_form')
def report_crime():
   return render_template('report_crime_form.html')

@app.route('/test')
def test():
   return render_template('table_template.html')

@app.route('/reported_crimes')
def view_reported_crime():
  profiles = Profile.query.all()
  return render_template('reported_crimes.html', profiles=profiles)

@app.route('/add', methods=["POST"])
def profile():
     
  
    full_name = request.form.get("full_name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    incident_description = request.form.get("incident")
    crime_category = request.form.get("crime_category")
    location = request.form.get("area")
    suspect_info = request.form.get("suspect_info")
    date_and_time = request.form.get("date_time")
    date_time= datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M')
    officer_in_charge = request.form.get("incident_handler")

 

    if full_name != '' and incident_description != '' and age is not None:
        p = Profile(full_name=full_name, age=age, gender=gender, phone=phone, incident_description=incident_description, crime_category=crime_category, location=location, suspect_info= suspect_info, date_and_time=date_time, officer_in_charge=officer_in_charge)
        db.session.add(p)
        db.session.commit()
        return redirect('/reported_crimes')
    else:
        return redirect('/reported_crimes')


@app.route('/predict', methods=['POST'])
def predict():
        
        int_features= [int (x) for x in request.form.values()]
        final_feat = [np.array(int_features)]
        pred = model.predict(final_feat)
        variety_mappings = {0: 'Break and Enter Commercial ', 1: 'Break and Enter Residential/Other', 2: 'Mischief', 3:'Other Theft',4:'Theft from Vehicle',5:'Theft of Bicycle',6:'Theft of Vehicle',7:'Vehicle Collision or Pedestrian Struck (with Fatality)',8:'Vehicle Collision or Pedestrian Struck (with Injury)'}
        for x in pred:
         val=x
        
        return render_template('prediction_form.html', data=format(variety_mappings[val]))

@app.route('/delete/<int:id>')
def erase(id):
     

    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/reported_crimes')

if __name__ == '__main__':
   app.run(debug=True)
  