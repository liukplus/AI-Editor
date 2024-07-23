from flask import Blueprint
from flask_cors import CORS

# 创建蓝图对象
richtext_bp = Blueprint('richtext', __name__, url_prefix='/richtext')
# 跨域
CORS(richtext_bp, supports_credentials=True)
