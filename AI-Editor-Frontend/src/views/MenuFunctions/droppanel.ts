import { Boot, IDomEditor, IDropPanelMenu } from "@wangeditor/editor"
import { DOMElement } from "@wangeditor/editor/dist/editor/src/utils/dom"
import axios from "axios"
import request from "@/utils/myrequest"
import $ from 'jquery'
import typewriter from "@/views/MenuFunctions/typewriter"
import { LoadingInstance } from "element-plus/es/components/loading/src/loading"
import { ElLoading } from "element-plus"
class MyDropPanelMenu implements IDropPanelMenu {    // TS 语法
// class MyDropPanelMenu {                           // JS 语法
    showDropPanel: boolean
    title: string
    iconSvg?: string | undefined
    hotkey?: string | undefined
    alwaysEnable?: boolean | undefined
    tag: string
    width?: number | undefined
    constructor() {
        this.title = 'AI'
        // this.iconSvg = '<svg >...</svg>'
        this.tag = 'button'
        this.showDropPanel = true
    }

    // 菜单是否需要激活（如选中加粗文本，“加粗”菜单会激活），用不到则返回 false
    isActive(editor: IDomEditor): boolean {    // TS 语法
    // isActive(editor) {                      // JS 语法
        return false
    }

    // 获取菜单执行时的 value ，用不到则返回空 字符串或 false
    getValue(editor: IDomEditor): string | boolean {    // TS 语法
    // getValue(editor) {                            // JS 语法
        return ''
    }

    // 菜单是否需要禁用（如选中 H1 ，“引用”菜单被禁用），用不到则返回 false
    isDisabled(editor: IDomEditor): boolean {   // TS 语法
    // isDisabled(editor) {                     // JS 语法
        return false
    }

    // 点击菜单时触发的函数
    exec(editor: IDomEditor, value: string | boolean) {   // TS 语法
    // exec(editor, value) {                              // JS 语法
        // DropPanel menu ，这个函数不用写，空着即可
    }

    // 定义 DropPanel 内部的 DOM Element
    getPanelContentElem(editor: IDomEditor): DOMElement {   // TS 语法
    // getPanelContentElem(editor) {                        // JS 语法
    
    const onconsume = (str:string) =>{
      editor.insertText(str)
    }
    const apilist = ["/api/ai_API/getpolish","/api/ai_API/getcontinuation","/api/ai_API/getTypesetting","/api/ai_API/generateTable","api/ai_API/generateUML","api/ai_API/getVisualization"]    
    const $list = $(`<ul class="w-e-panel-my-list">
            <li value="0">智能润色</li> 
            <li value="1">智能续写</li>
            <li value="2">智能排版</li>
            <li value="3">智能表格</li>
            <li value="4">智能UML建模</li>
            <li value="5">智能可视化</li>
          </ul>`)
        $list.on('click', 'li',  function() {
          // console.log(this.value)
          const formData = new FormData()
          const descendent = editor.getFragment()
          // if (descendent[0].children.length!=1){
          //   ElMessage.info("只能选择文本")
          //   return
          // }
          var selected = ""
          descendent.forEach((v)=>{
            selected += v.children[0].text
          })
          formData.append("content",selected)
          if (this.value==3){
            request({
              method:'post',
              url: apilist[this.value],
              data:formData,
            }).then(res => {
              editor.insertNode(res.data.data)
              ElMessage.success("已完成")
            })
          }else if(this.value==2){
            request({
              method:'post',
              url: apilist[this.value],
              data:formData,
            }).then(res => {
              editor.dangerouslyInsertHtml(res.data.data)
              ElMessage.success("已完成")
            })
          }else if(this.value>3){
            request({
              method:'post',
              url: apilist[this.value],
              data:formData,
            }).then(res => {
              editor.dangerouslyInsertHtml("<img src="+res.data.data.url+">")
              ElMessage.success("已完成")
            })
          }else{
            const tw = new typewriter(onconsume,apilist[this.value])
            tw.start()
            fetch(apilist[this.value],{method:'post',body:formData})
            .then((response) => {
              const reader = response.body.getReader();
              return new ReadableStream({
                start(controller) {
                  return pump();
                  function pump() {
                    return reader.read().then(({ done, value }) => {
                      if (done) {
                        setTimeout(() => ElMessage.success("已完成"),2000)
                        controller.close();
                        return;
                      }
                      tw.add(new TextDecoder().decode(value))
                      controller.enqueue(value);
                      return pump();
                    });
                  }
                },
              });
            })
            
          }
          
})

        return $list[0] // 返回 DOM Element 类型

        // PS：也可以把 $list 缓存下来，这样不用每次重复创建、重复绑定事件，优化性能
    }
}
const menuConf = {
    key: 'droppanel', // menu key ，唯一。注册之后，需通过 toolbarKeys 配置到工具栏
    factory() {
      console.log("register droppanel")
      return new MyDropPanelMenu()
    },
  }
Boot.registerMenu(menuConf)