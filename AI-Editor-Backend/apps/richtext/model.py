from apps import db
from sqlalchemy import UniqueConstraint

# 成绩模型类
class RichText(db.Model):
    __tablename__ = 'RichText'
    __table_args__ = (UniqueConstraint("user_id", "text_name",name="user_id__text_name"),)
    text_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_name=db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Account.id'),nullable=False)
