from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    toDo = db.relationship("ToDoList")

    def __init__(self, name, password):
        self.name = name
        self.password = password


class ToDoList(db.Model):
    __tablename__ = "toDoList"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.ForeignKey("user.id"))

    def __init__(self, text):
        self.text = text
