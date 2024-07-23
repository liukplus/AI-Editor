from apps import db


# 管理员账号模型类
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True,nullable=False, unique=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('Account.id'), primary_key=True, nullable=True)
    username = db.Column(db.String(80),nullable=False, unique=True)
    # name = db.Column(db.String(80), nullable=False)
    # admin_token = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return ('id:{},admin_id:{},username:{}').format(
            self.id,self.admin_id,self.username)