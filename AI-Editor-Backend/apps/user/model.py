from apps import db


# 用户信息模型类
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Account.user_id'), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # name = db.Column(db.String(80), nullable=False)
    # identification=db.Column(db.Enum('admin,common'),sever_default='common',nullable=False)    username = db.Column(db.String(80), unique=True, nullable=False)
    # 绩点

    def __repr__(self):
        return 'id: {}, user_id: {}, username: {}'.format(
            self.id,self.user_id, self.username)
