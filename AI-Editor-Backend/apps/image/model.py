from apps import db


# 创建专业信息模型类
class Image(db.Model):
    __tablename__ = 'Image'
    image_id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)

    text_id=db.Column(db.Integer,db.ForeignKey('RichText.text_id'),nullable=False)



