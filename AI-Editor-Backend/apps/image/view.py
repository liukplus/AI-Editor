# 导入包
from flask import request, jsonify
from apps.image.model import Image
from apps.image import image_bp
from apps import db
import os
import re
from apps.utils import localtoHttp

# 方法函数
@image_bp.route('/uploadimages', methods=['get', 'post'])
def uploadimages():#user_id,text_id
    fileItem=request.files.get('image')
    user_id=request.form.get('user_id')
    text_id=request.form.get('text_id')
    img=Image(
        #user_id=user_id,
        image_id=None, 
        text_id=text_id,
    )
    db.session.add(img)
    db.session.flush()
    db.session.commit()
    # url="D:\\aieditor\\database\\Resources\\"+str(user_id)+"\\imgs\\"+str(img.image_id)+".png"
    url = "http://localhost:5000/static/"+str(user_id)+"/imgs/"+str(img.image_id)+".png"
    alt = "D:\\backend\\score-management-system-back_end\\static\\"+str(user_id)+"\\imgs\\"+str(img.image_id)+".png"
    print(fileItem)
    fileItem.save(alt)
    tempmap={
        "errno":0,
        "data":{
            "url":url,
            "alt":alt,
            "href":""
        }
    }
    return jsonify(tempmap)

@image_bp.route('/deleteimages', methods=['get', 'post'])#将上面的alt字段和url返回给后端
def deleteimages():#user_id,text_id
    #fileItem=request.files['wangeditor-uploaded-image']
    url=request.form.get('url')
    res=int(request.form.get('alt'))
    user_exist = Image.query.filter_by(image_id=res).first()
    if user_exist is None:
        return jsonify({'code': 1, 'msg': 'image does not exist in database.'})
    else:
        db.session.delete(user_exist)
        db.session.commit()

    if os.path.exists(url):
        os.remove(url)
        return jsonify({'code': 200, 'msg': 'succeed to del.'})
    return jsonify({'code': 1, 'msg': 'url does not exist'})
