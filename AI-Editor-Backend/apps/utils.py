# 把性别由布尔值转换为中文
def sex_init(sex):
    if sex == 0:
        return '女'
    else:
        return '男'
def localtoHttp(localUrl):
    return localUrl.replace("D:\\aieditor\\database\\Resources\\","http://localhost:5000/staic/")
def httptoLocal(httpUrl):
    return httpUrl.replace("http://localhost:5000/static/","D:\\aieditor\\database\\Resources\\")
