import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import openai
import json

# 1. INITIALIZE THE APP (This must come before @app.route)
app = Flask(__name__)

# 2. DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. API KEY (Use your key or leave empty if using the "Mock" method below)
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# 4. DATABASE MODEL
class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200))
    plan_data = db.Column(db.Text) 
    progress = db.Column(db.Integer, default=0)

# Create the database file
with app.app_context():
    db.create_all()

# 5. ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_goal = request.form.get('goal')
    
    # MOCK DATA (Use this if you don't have a paid OpenAI key yet)
    # If you want to use real AI, uncomment the openai.ChatCompletion section from previous steps
    fake_ai_json = {
      "Day 1": {"subject": f"Intro to {user_goal}", "target": "Basics and Setup", "platform": "YouTube"},
      "Day 2": {"subject": "Core Fundamentals", "target": "First Practice Project", "platform": "Coursera"},
      "Day 3": {"subject": "Intermediate Logic", "target": "Coding Challenges", "platform": "Udemy"},
      "Day 4": {"subject": "Advanced Integration", "target": "API/Database basics", "platform": "LinkedIn"},
      "Day 5": {"subject": "Final Portfolio", "target": "Build and Deploy", "platform": "Github"}
    }
    
    new_plan = Curriculum(goal=user_goal, plan_data=json.dumps(fake_ai_json), progress=0)
    db.session.add(new_plan)
    db.session.commit()
    return redirect(url_for('dashboard', plan_id=new_plan.id))

@app.route('/dashboard/<int:plan_id>')
def dashboard(plan_id):
    plan = Curriculum.query.get(plan_id)
    curriculum_dict = json.loads(plan.plan_data)
    
    internships = []
    if plan.progress >= 60:
        internships = [
            {"title": "Junior Developer", "company": "TechCorp", "link": "https://www.linkedin.com/jobs"},
            {"title": "AI Intern", "company": "Future Systems", "link": "https://internshala.com"}
        ]
    
    return render_template('dashboard.html', plan=plan, subjects=curriculum_dict, internships=internships)

@app.route('/update/<int:plan_id>')
def update(plan_id):
    plan = Curriculum.query.get(plan_id)
    if plan.progress < 100:
        plan.progress += 20
    db.session.commit()
    return redirect(url_for('dashboard', plan_id=plan.id))

# 6. RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)