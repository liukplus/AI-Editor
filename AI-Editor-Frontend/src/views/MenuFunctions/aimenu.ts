// import {axios} from '../../utils/request'
// import { Boot } from '@wangeditor/editor'
// import $ from 'jquery'
// class AIMenu {
//   constructor() {
//     this.title = 'My menu'
//     // this.iconSvg = '<svg >...</svg>'
//     this.tag = 'button'
//     this.showDropPanel = true
// }

// // 菜单是否需要激活（如选中加粗文本，“加粗”菜单会激活），用不到则返回 false
// // isActive(editor: IDomEditor): boolean {    // TS 语法
// isActive(editor) {                      // JS 语法
//     return false
// }

// // 获取菜单执行时的 value ，用不到则返回空 字符串或 false
// // getValue(editor: IDomEditor): string | boolean {    // TS 语法
// getValue(editor) {                               // JS 语法
//     return ''
// }

// // 菜单是否需要禁用（如选中 H1 ，“引用”菜单被禁用），用不到则返回 false
// // isDisabled(editor: IDomEditor): boolean {   // TS 语法
// isDisabled(editor) {                     // JS 语法
//     return false
// }

// // 点击菜单时触发的函数
// // exec(editor: IDomEditor, value: string | boolean) {   // TS 语法
// exec(editor, value) {                              // JS 语法
//     // DropPanel menu ，这个函数不用写，空着即可
// }

// // 定义 DropPanel 内部的 DOM Element
// // getPanelContentElem(editor: IDomEditor): DOMElement {   // TS 语法
// getPanelContentElem(editor) {                        // JS 语法
//     const $list = $(`<ul class="w-e-panel-my-list">
//         <li>北京</li> <li>上海</li> <li>深圳</li>
//       </ul>`)

//     $list.on('click', 'li', function () {
//       editor.insertText(this.innerHTML)
//       editor.insertText(' ')
//     })

//     return $list[0] // 返回 DOM Element 类型

//     // PS：也可以把 $list 缓存下来，这样不用每次重复创建、重复绑定事件，优化性能
// }
//     // constructor() {
//     //     this.title = 'AI',
//     //     this.tag = 'button'
        
//     // }
//     // getValue() { return '' }
//     // isActive() { return false }
//     // isDisabled() { return false }
//     // exec(editor) {
        
//     //     axios({
//     //                 method:'post',
//     //                 url:'/getcontinuation',
//     //                 data:{
//     //                 "username":"leo_",
//     //                 "key":"48b357e416a78be940f51b8e39f933984bb5bb42",
//     //                 "cont":editor.Fragment()[0].children.text}
//     //                 //
//     //             }).then(res=>{    
//     //                 console.log(res.answer)    
//     //                 editor.insertText(res.answer)
//     // })

//     // }
// }
// const menuConf = {
//   key: 'AI', // menu key ，唯一。注册之后，需通过 toolbarKeys 配置到工具栏
//   factory() {
//     console.log("register AI")
//     return new AIMenu()
//   },
// }
// Boot.registerMenu(menuConf)

  