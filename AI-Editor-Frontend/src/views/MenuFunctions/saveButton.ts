import { IButtonMenu, IDomEditor } from '@wangeditor/editor'
import { Boot } from '@wangeditor/editor'
import request from "@/utils/myrequest"
import axios from 'axios'
import router from '@/router'
class MyButtonMenu implements IButtonMenu {
// class MyButtonMenu {                       // JS 语法
    title: string
    iconSvg?: string | undefined
    hotkey?: string | undefined
    alwaysEnable?: boolean | undefined
    tag: string
    width?: number | undefined
    constructor() {
        this.title = 'save' // 自定义菜单标题
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
        const html = editor.getHtml()
        const formData = new FormData()
        formData.append("content",html)
        formData.append("text_name","test1")
        request({
          method:'post',
          url: "api/richtext/upload_richtext",
          data:formData,
          headers:{"Content-Type":'multipart/form-data'}
        }).then(res => {
          localStorage.setItem(router.currentRoute.value.query.file_name, html)
          ElMessage.success("保存成功")
        },() => ElMessage.warning("保存失败"))
    }

}
const menu1Conf = {
  key: 'save', // 定义 menu key ：要保证唯一、不重复（重要）
  factory() {
    return new MyButtonMenu() // 把 `YourMenuClass` 替换为你菜单的 class
  },
}
Boot.registerMenu(menu1Conf)