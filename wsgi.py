from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, render_template
from flask_restful import Api
from models import Task, SprintPending, SprintComplete, engine

Session = sessionmaker(bind=engine)

app = Flask(__name__)
api = Api(app)


@app.route('/CheckData', methods=['POST', 'GET'])
def post():
    with Session() as session:
        if request.method == 'POST':
            new_task = Task(task=request.form['task'], bug=request.form['bug'], week=1)
            session.add(new_task)
            session.commit()
            return {"message": new_task.id}

        tasks = session.query(Task)
        sprint = session.query(SprintPending).all()
        return render_template("form.html", value=tasks, sprints=sprint)


@app.route("/check", methods=["POST"])
def get():
    with Session() as session:
        if request.method == 'POST':
            # Python 3
            payload = request.form.get("task_bug").split(" ")
            new_sprint = SprintPending(task=payload[0], bug=payload[1])
            session.add(new_sprint)
            session.commit()
            return {"message": new_sprint.id}


@app.route("/status", methods=["POST"])
def put():
    with Session() as session:
        if request.method == 'POST':
            complete_sprint = session.query(SprintPending).filter(SprintPending.id == request.form.get("sprint")).first()
            session.add(SprintComplete(task=complete_sprint.task, bug=0))
            session.delete(complete_sprint)
            session.commit()
            return {"message": "update"}


if __name__ == "__main__":
    app.run(debug=True)


