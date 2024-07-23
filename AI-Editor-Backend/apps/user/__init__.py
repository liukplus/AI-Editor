from flask import Blueprint
from flask_cors import CORS

# 创建蓝图对象
user_bp = Blueprint('user', __name__, url_prefix='/user')
# 跨域
CORS(user_bp, supports_credentials=True)
