from flask import Flask, render_template # importing templates
from flask_sqlalchemy import SQLAlchemy # importing db manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # init db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to prevent error
db = SQLAlchemy(app)  # creating db


class Todo(db.Model):  # class for todo items
    id = db.Column(db.Integer, primary_key=True)   # for each entry needs a column, unique value for each to do item created
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    # show all todos
    todo_list = Todo.query.all()  # query the todo lists
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


if __name__ == "__main__":
    db.create_all() # creates the db.sqlite file

    new_todo = Todo(title="Todo 1", complete=False)
    db.session.add(new_todo)
    db.session.commit()
    app.run(debug=True)
