from flask import Blueprint
from flask_cors import CORS

# 创建蓝图对象
image_bp = Blueprint('image', __name__, url_prefix='/image')
# 跨域
CORS(image_bp, supports_credentials=True)
