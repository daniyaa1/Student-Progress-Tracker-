from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    due = db.Column(db.String(10))
    subj = db.Column(db.String(50))
    done = db.Column(db.Boolean, default=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET','POST'])
def api_tasks():
    if request.method=='POST':
        data=request.json
        t=Task(name=data['name'],due=data['due'],subj=data.get('subj',''),done=False)
        db.session.add(t); db.session.commit()
    return jsonify([{'id':t.id,'name':t.name,'due':t.due,'subj':t.subj,'done':t.done} for t in Task.query.all()])

@app.route('/api/tasks/<int:id>', methods=['PUT','DELETE'])
def api_task(id):
    t=Task.query.get_or_404(id)
    if request.method=='PUT':
        data=request.json
        t.name, t.due, t.subj, t.done = data['name'], data['due'], data.get('subj',''), data['done']
        db.session.commit()
        return jsonify(ok=True)
    db.session.delete(t); db.session.commit()
    return jsonify(ok=True)

if __name__=='__main__':
    app.run(debug=True)
