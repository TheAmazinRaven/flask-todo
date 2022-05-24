from flask import Flask, render_template, request, redirect, url_for  # importing templates
from flask_sqlalchemy import SQLAlchemy  # importing db manager

app = Flask(__name__)

# /// = relative path, //// = absolute path

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # init db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to prevent error
db = SQLAlchemy(app)  # creating db


class Todo(db.Model):  # class for todo items
    id = db.Column(db.Integer, primary_key=True)   # for each entry needs a column, unique value for each to do item created
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    # show all todos
    todo_list = Todo.query.all()  # query the todo lists
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()  # creates the db.sqlite file

    # new_todo = Todo(title="Todo 1", complete=False)
    # db.session.add(new_todo)
    # db.session.commit()
    app.run(debug=True)
