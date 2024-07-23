import erniebot
from apps import db
from flask import Flask, json, request, jsonify, stream_with_context
from paddleocr import PaddleOCR, draw_ocr
from apps.aiAPI import ai_api_bp
from apps.image.model import Image
import os
import json
from apps.utils import localtoHttp
ocr = PaddleOCR(
    cls_model_dir='D:\paddleocr\whl\cls\ch_ppocr_mobile_v2.0_cls_infer',
    det_model_dir='D:\paddleocr\whl\det\ch\ch_PP-OCRv4_det_infer',
    rec_model_dir='D:\paddleocr\whl\\rec\ch\ch_PP-OCRv4_rec_infer',
    use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
AIMODEL_KEY = "48b357e416a78be940f51b8e39f933984bb5bb42"
erniebot.api_type = 'aistudio'
def JsonToTableContent(data):
    size=data["size"]
    head={"type":"table-row","children":[]}
    res={"type":"table",
        "width":"auto",
         "children":[head,]}
    for key in data['head']:
        head["children"].append({"isHeader":True,"type":"table-cell","children":[{"text":key}]})
    for row in range(size[0]):
        res["children"].append({"type":"table-row","children":[]})
        for column in range(size[1]):
            print(column)
            (res["children"][row+1]["children"]
             .append({"type":"table-cell","children":
                [{"text":data["content"][row][column]}]}))
    return jsonify({"data":res,"code":200,"msg":"success"})

def generate_mermaid_image(mermaid_code, output_path):
    with open("temp.mmd", "w") as file:
        file.write(mermaid_code)
    os.system(f"mmdc -i temp.mmd -o {output_path}")
    os.remove("temp.mmd")

@ai_api_bp.route('/getpolish', methods=["GET", "POST"])
def getpolish():
    # 获取用户提问内容
    quescont = request.form.get("content")
    print(request)
    askcont="帮我润色下面这段话并且只返回内容不允许有附加内容:"+quescont

    erniebot.access_token = AIMODEL_KEY
    # try:
    #     response = erniebot.ChatCompletion.create(
    #         model='ernie-bot',
    #         messages=[{'role': 'user', 'content':askcont}],
    #     )
    #     restext = response['result']
    #     webdict = {'data': restext}
    #     return jsonify(webdict)
    # except:
    #     return "error"
    def generate():
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
            stream=True
        )
        for data in response:
            yield data['result']
    return stream_with_context(generate())
    

@ai_api_bp.route('/getcontinuation', methods=["GET", "POST"])
def getcontinuation():
    # 获取用户名
    print(request)
    username= request.form.get("username")
    # 获取用户的访问令牌
    print(username)
    key = request.form.get("key")
    # 获取用户提问内容
    print(key)
    quescont = request.form.get("content")
    print(quescont)
    askcont="帮我续写下面这段话,只需要一段内容不需要任何其他辅助信息,且不能包含原有的文字，忽略每一次续写任务的上下文:"+quescont

    erniebot.access_token = AIMODEL_KEY

    def generate():
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': askcont}],
            stream=True
        )
        for data in response:
            yield data['result']
        # except:
        #     return jsonify({"data": None, "code": 1, "msg": "Failure"})
    return stream_with_context(generate())

@ai_api_bp.route('/generateTable',methods=['get','post'])
def generateTable():
    content = request.form.get("content")
    prompt=("根据冒号之后的内容提取成表格信息并返回，返回格式为json文件，且不返回任何其他信息。包含属性为head，content，size。size为长度为"
            "2的数组，其中第一个数字是不包含表头的行数，第二个数字是列数。head为一个字符串数组，给出表头信息。content为一个二维数组，每个元素为对应表格的字符串：")
    ask=prompt+content
    erniebot.access_token = AIMODEL_KEY
    # try:
        # 从大模型获取回答
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': ask}],
    )
    data=response['result'][7:-3]
    data2=""
    for line in data.splitlines():
        data2=data2+line
    print(data2)
    return JsonToTableContent(json.loads(data2))
    # except Exception as e:
    #     print(e)
    #     return {"data":None,"code":1,"msg":"failure"}
@ai_api_bp.route('/getOCR',methods=['get','post'])
def getOCR():
    img_path = request.form.get("alt")
    result = ocr.ocr(img_path, cls=True)
    data = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            data.append(line[-1][0])
    return jsonify({"data":json.dumps(data)})
@ai_api_bp.route('/generateUML', methods=['get','post'])
def generateUML():
    # 获取用户令牌
    user_id=request.form.get("user_id")
    text_id=request.form.get("text_id")
    content = request.form.get("content")
    # 生成mermaid语言
    ask = "请根据以下内容生成mermaid语法的代码，用于绘制UML图，你的回答应该只包含代码，不要输出任何除mermaid代码以外的符号或解释文字，你的回答中不能出现中文，只能使用英文：" + content
    print(ask)
    # 调用模型
    erniebot.access_token = AIMODEL_KEY
    try:
        # 从大模型获取回答
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': ask}],
        )
        restext = response['result']
        restext.replace('\n',' ')
        index_start = restext.find("```mermaid")
        index_end = restext.find("```", index_start + 1)
        print(index_end)
        print("index_start: " + str(index_start) + ", index_end: " + str(index_end))
        mmc = restext[index_start + 10 : index_end]
        print(mmc)
    except:
        return "error"
    # 调用mermaid生成图片
    img = Image(
        text_id=text_id,
    )
    db.session.add(img)
    db.session.flush()
    db.session.commit()
    url = "D:\\backend\\score-management-system-back_end\\static\\" + str(user_id) + "\\imgs\\" + str(img.image_id) + ".png"
    furl = "http://localhost:5000/static/"+str(user_id)+"/imgs/"+str(img.image_id)+".png"
    generate_mermaid_image(mmc, url)
    tempmap = {
        "errno": 0,
        "data": {
            "url": furl,
            "alt": str(img.image_id),
            "href": ""
        }
    }
    return jsonify(tempmap)
# async def async_os():

@ai_api_bp.route('/getVisualization',methods=['get','post'])
def getVisualization():

    user_id=request.form.get('user_id')
    text_id=request.form.get("text_id")
    img = Image(
        text_id=text_id,
    )
    db.session.add(img)
    db.session.flush()
    db.session.commit()
    erniebot.access_token = AIMODEL_KEY
    url = "D:\\backend\\score-management-system-back_end\\static\\" + str(user_id) + "\\imgs\\" + str(img.image_id) + ".png"
    furl = "http://localhost:5000/static/"+str(user_id)+"/imgs/"+str(img.image_id)+".png"
    prompt = (
            "将冒号后的文本进行提取成数据，并且在python语言中定义上述数据，"
            "利用matplotlib库生成图片并保存为"+url+"。要求图中有图例和英变量名并且全部为英文，并且数据要进行归一化，不要写show语句。")
    stream = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompt+ request.form.get("content")}],
        system="你是一个数据分析师。"
    )
    text = stream['result']
    index_start = text.find("```python")
    index_end = text.find("```", index_start + 1)
    print(text[index_start + 9:index_end])
    with open('D:\\backend\\score-management-system-back_end\\static\\generateVis.py','w+',encoding='utf-8') as f:
        f.write(text[index_start+9:index_end].replace("plt.show()","         "))
        f.close()
    os.system("python D:\\backend\\score-management-system-back_end\\static\\generateVis.py")
    print("os system后的内容")
    # exec(text[index_start + 9:index_end].replace("plt.show()", "         "))
    tempmap = {
        "errno": 0,
        "data": {
            "url": furl,
            "alt": str(img.image_id),
            "href": ""
        }
    }
    return jsonify(tempmap)
@ai_api_bp.route('/getTypesetting',methods=['get','post'])
def getTypesetting():
    content=request.form.get("content")
    prompt="将文本插入到HTML代码中，合理设置这段代码的字体行距等使得它变得美观，并返回HTML代码，不要有遗漏，不要返回任何其他信息。下面是要嵌入的文本："
    erniebot.access_token = AIMODEL_KEY
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': prompt+content}],
        )
        text = response['result']
        index_start = text.find("```html")
        index_end = text.find("```", index_start + 1)
        text = text[index_start+7:index_end]
        print(text)
        return jsonify({"data": text, 'code': "200", 'msg': "success"})
    except Exception as e:
        print(e)
        return jsonify({"data": None, "code": 1, "msg": "Failure"})