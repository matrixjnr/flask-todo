from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


# Create a Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(200), nullable=False)


@app.route('/')
def index():
    # Retrieve Todo items from the database
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        task = request.form['task']
        if task:
            new_todo = Todo(task=task)
            db.session.add(new_todo)
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
