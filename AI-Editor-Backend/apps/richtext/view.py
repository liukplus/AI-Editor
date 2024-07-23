# 导入包
from operator import and_
import os.path

from flask import request, jsonify
# 导入模块
from apps import db
from apps.richtext import richtext_bp

# 导入模型类，方法
from apps.richtext.model import RichText


# 注册视图函数
# 筛选成绩信息
@richtext_bp.route('/get_richtext', methods=['GET', 'POST'])
def get_richtext():
    user_id=request.form.get('user_id')
    text_id=request.form.get('text_id')
    url="D:\\aieditor\\database\\Resources\\" + str(user_id) + "\\RichText\\" + str(text_id) + ".txt"
    if os.path.exists(url):
        with open(url, 'r') as file:
            html_content = file.read()
            file.close()
            return {"code":200,"data":html_content,"msg":"success."}
    else:
        return {"code":1,"data":None,"msg":"path does not exist."}

@richtext_bp.route('/get_richtext_list',methods=['GET','POST'])
def get_richtext_lists():
    user_id=request.form.get('user_id')
    query=RichText.query.filter(RichText.user_id==user_id).all()
    res=[]
    for ele in query:
        print(ele)
        each={}
        each['text_id']=ele.text_id
        each['text_name']=ele.text_name
        each['user_id']=ele.user_id
        res.append(each)
    return {"code":200,"data":res,"msg":"success."}
# 添加成绩
@richtext_bp.route('/upload_richtext', methods=['POST'])
def upload_richtext():
    user_id=request.form.get('user_id')
    text_name=request.form.get('text_name')
    content=request.form.get('content')

    query = RichText.query.filter(and_(RichText.user_id == user_id,RichText.text_name==text_name)).first()
    richtext = RichText(
        user_id=user_id,
        text_name=text_name,
    )
    if query==None:
        db.session.add(richtext)
        db.session.flush()
        db.session.commit()
    url = "D:\\aieditor\\database\\Resources\\" + str(user_id) + "\\RichText\\" + str(richtext.text_id) + ".txt"
    with open(url,'w+') as file:
        file.write(content)
    return jsonify({'code': 200, 'msg': 'succeed to upload.',"data":{"text_id":richtext.text_id}})

# 修改成绩
@richtext_bp.route('/del_richtext', methods=['POST'])
def del_richtext():
    pass



