from app import db

class User(db.Model):
    __tablename__ = 'user' #Must be defined the table name

    user_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Username: {}, Email: {}, Password: {}>".format(self.username, self.email, self.password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        users = User.query.all()
        result = []
        for user in users:
            obj = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'password':user.password
            }
            result.append(obj)
        return result

    def delete(self):
        db.session.delete(self)
        db.session.commit()
