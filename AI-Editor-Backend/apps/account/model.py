from apps import db


# 用户账号模型类
class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,unique=True)
    username = db.Column(db.String(80))
    # email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return 'username: {} role: {}'.format(self.username, self.role)
