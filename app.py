from flask import Flask
from flask_restful import Api
from models import db
from resources.task import TaskListResource, TaskResource, TaskCompleteResource, TaskResourceDelete

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db.init_app(app)

api = Api(app)

# Register routes
api.add_resource(TaskListResource, '/')
api.add_resource(TaskResource, '/task/<int:id>')
api.add_resource(TaskResourceDelete, '/delete/<int:id>')
api.add_resource(TaskCompleteResource, '/complete/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)
