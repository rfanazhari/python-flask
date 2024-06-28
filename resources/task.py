from flask import request, redirect, render_template,make_response
from flask_restful import Resource
from models import db, Todo

class TaskListResource(Resource):
    def get(self):
        tasks = Todo.query.order_by(Todo.created_at).all()
        return make_response(render_template('home.html', tasks=tasks))

    def post(self):
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

class TaskResource(Resource):
    def get(self, id):
        task = Todo.query.get_or_404(id)
        return make_response(render_template('update.html', task=task))

    def post(self, id):
        task = Todo.query.get_or_404(id)
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task'

    def delete(self, id):
        task_to_delete = Todo.query.get_or_404(id)
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue deleting the task'

class TaskResourceDelete(Resource):
    def get(self, id):
        task_to_delete = Todo.query.get_or_404(id)
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue deleting the task'

class TaskCompleteResource(Resource):
    def get(self, id):
        task_to_complete = Todo.query.get_or_404(id)
        try:
            task_to_complete.completed = 1
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue completing the task'
