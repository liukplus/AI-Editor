# 导入包
from flask import request, jsonify
# 导入模块
from apps import db
from apps.user import user_bp
from apps.user.model import User
from apps.account.model import Account

# 导入方法
from apps.utils import sex_init


# 定义方法函数
# 获取全部学生信息
def get_all_users():
    # 获取学生信息
    user_info = User.query.all()
    data = []
    for i in user_info:
        data.append(
            {
                'id':i.id,
                'user_id': i.user_id,
                'username': i.username,

            })
    # 返回用户信息
    return jsonify({'code': 200, 'msg': '获取成功', 'data': data})


# 筛选学生信息
def get_user_info(username):
    # 查询数据库中是否存在数据
    user_exist = User.query.filter_by(username=username).first()
    # 打印查询结果
    print(user_exist)
    if user_exist is None:
        return jsonify({'code': 1, 'msg': '用户信息为空'})
    else:
        data = [
            {
                'user_id': {'title': 'id', 'value': user_exist.user_id},
                'username': {'title': 'name', 'value': user_exist.name},
            },
            # {
            #     'address': {'title': '地址', 'value': stu_exist.address},
            #     'college': {'title': '学院', 'value': stu_exist.college},
            #     'major': {'title': '专业', 'value': stu_exist.major},
            #     'credits': {'title': '学分', 'value': stu_exist.credits},
            #     'GPA': {'title': '绩点', 'value': stu_exist.GPA}
            # }

        ]
        return jsonify({'code': 200, 'msg': '获取成功', 'data': data})


# 注册视图函数
# 获取学生信息
@user_bp.route('/get', methods=['GET', 'POST'])
def get_stu_info():
    if request.method == 'GET':
        data = get_all_users()
        return data
    else:
        username = request.form.get('username')#根据username选取
        data = get_user_info(username)
        return data


# 修改用户信息
@user_bp.route('/update', methods=['POST'])
def update_info():
    stu_id = request.form.get('user_id')
    user_exist = User.query.filter_by(user_id=stu_id).first()
    if user_exist is None:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    else:
        # 修改用户某条信息
        for item in request.form:
            if item == 'username':
                continue
            else:
                setattr(user_exist, item, request.form.get(item))
        db.session.commit()
        return jsonify({'code': 200, 'msg': '修改成功', 'data': user_exist})


# 添加信息
@user_bp.route('/add', methods=['POST'])
def add_info():
    user_id = request.form.get('user_id')
    user_exist = User.query.filter_by(user_id=user_id).first()
    if user_exist:
        return jsonify({'code': 1, 'msg': '用户已存在'})
    else:
        # 创建数据映射到数据库
        user = User(
            id=None,
            user_id=user_id,
            username=request.form.get('username'),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '添加成功', 'data': user})


# 删除信息
@user_bp.route('/delete', methods=['POST'])
def delete_info():
    user_id = request.form.get('user_id')
    user_exist = User.query.filter_by(user_id=user_id).first()
    if user_exist is None:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    else:
        db.session.delete(user_exist)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '删除成功', 'data': user_exist})
