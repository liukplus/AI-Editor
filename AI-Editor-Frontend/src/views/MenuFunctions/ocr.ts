// import {axios} from '../../utils/request'
// import { Boot } from '@wangeditor/editor'
// class AIMenu {
//     constructor() {
//         this.title = 'OCR',
//         this.tag = 'button'
        
//     }
//     getValue() { return '' }
//     isActive() { return false }
//     isDisabled() { return false }
//     exec(editor) {
//       descendent = editor.getFragment()
//       if (descendent.length!=0){
//         alert("只能选择单个图片")
//       }
//       selected = descendent[0]
//       url = selected.url
//       axios({
//               method:'post',
//               url:'/getocr',
//               data:{
//               "cont":url
//             }
//             }).then(res=>{    
//             console.log(res.answer)    
//             editor.insertText(res.answer)
//         })
//     }
// }
// const menuConf = {
//   key: 'ocr', // menu key ，唯一。注册之后，需通过 toolbarKeys 配置到工具栏
//   factory() {
//     console.log("register ocr")
//     return new AIMenu()
//   },
// }
// Boot.registerMenu(menuConf)
import { IButtonMenu, IDomEditor } from '@wangeditor/editor'
import { Boot } from '@wangeditor/editor'
import axios from 'axios'
import request from "@/utils/myrequest"
class MyButtonMenu implements IButtonMenu {
// class MyButtonMenu {                       // JS 语法
    title: string
    iconSvg?: string | undefined
    hotkey?: string | undefined
    alwaysEnable?: boolean | undefined
    tag: string
    width?: number | undefined
    constructor() {
        this.title = 'ocr' // 自定义菜单标题
        // this.iconSvg = '<svg>...</svg>' // 可选
        this.tag = 'button'
    }

    // 获取菜单执行时的 value ，用不到则返回空 字符串或 false
    getValue(editor: IDomEditor): string | boolean {   // TS 语法
    // getValue(editor) {                              // JS 语法
        return ' hello '
    }

    // 菜单是否需要激活（如选中加粗文本，“加粗”菜单会激活），用不到则返回 false
    isActive(editor: IDomEditor): boolean {  // TS 语法
    // isActive(editor) {                    // JS 语法
        return false
    }

    // 菜单是否需要禁用（如选中 H1 ，“引用”菜单被禁用），用不到则返回 false
    isDisabled(editor: IDomEditor): boolean {   // TS 语法
    // isDisabled(editor) {                     // JS 语法
        return false
    }

    // 点击菜单时触发的函数
    exec(editor: IDomEditor, value: string | boolean) {   // TS 语法
    // exec(editor, value) {                              // JS 语法
    const descendent = editor.getFragment()
    console.log(descendent[0].children[0])
    if (descendent[0].children.length!=1 || descendent[0].children[0].type!="image"){
      ElMessage.warning("只能选择单个图片")
    }
    const selected = descendent[0]
    const alt = selected.children[0].alt
    const url = selected.children[0].url
    var form = new FormData()
    console.log(alt)
    console.log(url)
    form.append("alt",alt)
    request({
            method:'post',
            url:'/api/ai_API/getOCR',
            data:form
          }).then(res => {
            JSON.parse(res.data.data).forEach((val:string)=>{
              editor.insertText(val+"\n")
            })
      })
    }

}
const menu1Conf = {
  key: 'ocr', // 定义 menu key ：要保证唯一、不重复（重要）
  factory() {
    return new MyButtonMenu() // 把 `YourMenuClass` 替换为你菜单的 class
  },
}
Boot.registerMenu(menu1Conf)