from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding task'
        
    else:
        tasks = Todo.query.order_by(Todo.created_at).all()
        return render_template('home.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue delete the task of '+task_to_delete.content

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue update the task of '+task.content
    else:
        return render_template('update.html', task=task)

@app.route('/complete/<int:id>')
def complete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        task_to_delete.completed = 1
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue delete the task of '+task_to_delete.content

if __name__ == "__main__":
    app.run(debug=True)