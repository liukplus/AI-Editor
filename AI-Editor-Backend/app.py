# 导入模块
import os
from flask import Flask, send_from_directory
from apps import create_app

app = create_app()
if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, host='0.0.0.0', port=5000)
