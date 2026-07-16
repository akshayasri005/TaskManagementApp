from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'taskmanagement123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- USER TABLE ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ---------------- TASK TABLE ----------------

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="Pending")

# ---------------- HOME ----------------

@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            return redirect('/dashboard')

        return "Invalid Username or Password"

    return render_template('login.html')

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    tasks = Task.query.all()

    return render_template(
        'dashboard.html',
        tasks=tasks
    )

# ---------------- ADD TASK ----------------

@app.route('/add', methods=['GET','POST'])
def add_task():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']

        task = Task(
            title=title,
            description=description
        )

        db.session.add(task)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('add_task.html')

# ---------------- EDIT TASK ----------------

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_task(id):

    task = Task.query.get(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.description = request.form['description']

        db.session.commit()

        return redirect('/dashboard')

    return render_template(
        'edit_task.html',
        task=task
    )

# ---------------- DELETE TASK ----------------

@app.route('/delete/<int:id>')
def delete_task(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/dashboard')

# ---------------- MAIN ----------------

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)