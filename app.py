from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    create = db.Column(db.DateTime, default= datetime.utcnow)

    def __rep__(self) -> str:
        return f"Task {self.id}"
    
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = User(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"
    else:
        tasks = User.query.order_by(User.create).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id:int):
    task_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"
    
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id:int):
    task = User.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem updating that task"
    else:
        return render_template("update.html", task=task)

if __name__ == "__main__":
    
    app.run(debug=True)
