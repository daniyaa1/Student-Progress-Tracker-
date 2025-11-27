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
    milestone = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(10), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET','POST'])
def api_tasks():
    if request.method=='POST':
        data=request.json
        t=Task(name=data['name'],due=data.get('due',''),subj=data.get('subj',''),done=False, milestone=data.get('milestone', False), notes=data.get('notes',''), priority=data.get('priority','medium'))
        db.session.add(t); db.session.commit()
    return jsonify([{
        'id':t.id,
        'name':t.name,
        'due':t.due,
        'subj':t.subj,
        'done':t.done,
        'milestone': bool(t.milestone),
        'notes': t.notes,
        'priority': t.priority,
        'created_at': t.created_at.isoformat() if t.created_at else None,
        'updated_at': t.updated_at.isoformat() if t.updated_at else None
    } for t in Task.query.order_by(Task.created_at.asc()).all()])

@app.route('/api/tasks/<int:id>', methods=['PUT','DELETE'])
def api_task(id):
    t=Task.query.get_or_404(id)
    if request.method=='PUT':
        data=request.json
        t.name = data.get('name', t.name)
        t.due = data.get('due', t.due)
        t.subj = data.get('subj', t.subj)
        t.done = data.get('done', t.done)
        # allow toggling/setting milestone from the client
        if 'milestone' in data:
            t.milestone = bool(data.get('milestone'))
        t.notes = data.get('notes', t.notes)
        t.priority = data.get('priority', t.priority)
        db.session.commit()
        return jsonify(ok=True)
    db.session.delete(t); db.session.commit()
    return jsonify(ok=True)


@app.route('/health')
def health():
    return 'ok', 200

if __name__=='__main__':
    # Ensure database tables are created within the application context
    with app.app_context():
        db.create_all()
        # Ensure any new columns are added to existing SQLite table (simple dev-time migration)
        try:
            from sqlalchemy import inspect
            insp = inspect(db.engine)
            cols = [c['name'] for c in insp.get_columns('task')]
        except Exception:
            cols = []
        # If table exists but missing new columns, attempt to add them (SQLite supports ADD COLUMN)
        alter_sql = []
        if 'notes' not in cols:
            alter_sql.append("ALTER TABLE task ADD COLUMN notes TEXT")
        if 'priority' not in cols:
            alter_sql.append("ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium'")
        if 'milestone' not in cols:
            # SQLite uses integer booleans; default to 0 (false)
            alter_sql.append("ALTER TABLE task ADD COLUMN milestone BOOLEAN DEFAULT 0")
        if 'created_at' not in cols:
            alter_sql.append("ALTER TABLE task ADD COLUMN created_at DATETIME")
        if 'updated_at' not in cols:
            alter_sql.append("ALTER TABLE task ADD COLUMN updated_at DATETIME")
        for s in alter_sql:
            try:
                db.engine.execute(s)
            except Exception:
                pass
    app.run(debug=True)
