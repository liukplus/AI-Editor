from flask import Blueprint
from flask_cors import CORS

# 创建蓝图对象
ai_api_bp = Blueprint('ai_API', __name__, url_prefix='/ai_API')
# 跨域
CORS(ai_api_bp, supports_credentials=True)
