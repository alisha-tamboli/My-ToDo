from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


USERNAME = 'admin'
PASSWORD = 'password123'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # print(request.form['title])
        title_var = (request.form['title'])
        desc_var = (request.form['desc'])
        todo = Todo(title = title_var, desc = desc_var)
        db.session.add(todo) 
        db.session.commit()
    allTodo = Todo.query.all()   
    return render_template('index.html', allTodo = allTodo)


@app.route('/update/<int:sno>' , methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo) 
        db.session.commit()  
        return redirect("/")

    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html', todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password are correct
        if username == USERNAME and password == PASSWORD:
            # Store login state in the session
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    # Remove the login state from the session
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True)
