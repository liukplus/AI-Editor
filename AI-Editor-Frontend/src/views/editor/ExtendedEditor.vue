<script setup>
// import { h } from 'snabbdom'
import { onBeforeUnmount, ref, shallowRef } from 'vue'
// import { IButtonMenu } from '@wangeditor/core'
// import '@/views/MenuFunctions/aimenu'
import '@/views/MenuFunctions/ocr'
import '@/views/MenuFunctions/droppanel'
import '@/views/MenuFunctions/saveButton'
import axios from 'axios'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import formulaModule from '@wangeditor/plugin-formula'
import {Boot} from '@wangeditor/editor'
import markdownModule from "@wangeditor/plugin-md"
import request from "@/utils/myrequest"
import route from "@/router"
// 测试：第三方插件
// import withCtrlEnter from '@wangeditor/plugin-ctrl-enter'
// Boot.registerPlugin(withCtrlEnter)

// // 测试：多语言
// i18nChangeLanguage('en')

// // 测试：注册 renderElem
// function renderElemFn(elem, children) {
//     const vnode = h('div', {}, children) // type: 'paragraph' 节点，即渲染为 <p> 标签
//     return vnode
// }
// const renderElemConf = {
//     type: 'paragraph', // 节点 type ，重要！！！
//     renderElem: renderElemFn,
// }
// Boot.registerRenderElem(renderElemConf)

// // 测试：注册插件
// function withCtrlEnter(editor) {
//     const { insertBreak } = editor

//     setTimeout(() => {
//         // beforeInput 事件不能识别 ctrl+enter ，所以自己绑定 DOM 事件
//         const { $textArea } = DomEditor.getTextarea(newEditor)
//         $textArea.on('keydown', e => {
//             const isCtrl = e.ctrlKey || e.metaKey
//             if (e.keyCode === 13 && isCtrl) {
//                 // ctrl+enter 触发换行
//                 editor.insertBreak()
//             } 
//         })
//     })

//     const newEditor = editor
//     newEditor.insertBreak = () => {
//         const e = window.event
//         const isCtrl = e.ctrlKey || e.metaKey
//         // 只有 ctrl 才能换行
//         if (isCtrl) {
//             insertBreak()
//         }
//     }
//     return newEditor
// }
// Boot.registerPlugin(withCtrlEnter)

// 测试：注册 button menu





// 编辑器配置
// function customCheckImageFn(src: string, alt: string, url: string): boolean | undefined | string { // TS 语法
function customCheckImageFn(src, alt, url) {
    console.log("customCheckImageFn"+src+alt+url)                                                    // JS 语法
    if (!src) {
        return
    }
    if (src.indexOf('http') !== 0) {
        return '图片网址必须以 http/https 开头'
    }
    return true

    // 返回值有三种选择：
    // 1. 返回 true ，说明检查通过，编辑器将正常插入图片
    // 2. 返回一个字符串，说明检查未通过，编辑器会阻止插入。会 alert 出错误信息（即返回的字符串）
    // 3. 返回 undefined（即没有任何返回），说明检查未通过，编辑器会阻止插入。但不会提示任何信息
}

// 转换图片链接
// function customParseImageSrc(src: string): string {  // TS 语法
function customParseImageSrc(src) {               // JS 语法
    console.log("customParseImageSrc"+src)
    if (src.indexOf('http') !== 0) {
        return `http://${src}`
    }
    return src
}
// axios.post("http://localhost:5173/api/upload").then(
//         (response) => {
//           console.log("请求成功了", response.data);
//         })
const editorConfig = {
    placeholder: 'Type Here...',
    MENU_CONF: {
        insertImage: {
            // checkImage(src) {
            //     console.log('image src', src)
            //     if (src.indexOf("http") !== 0) {
            //         return "图片网址必须以 http/https 开头";
            //     }
            //     return true;
            // },
        onInsertedImage(imageNode) {
            console.log("imageNode"+imageNode)                    // JS 语法
            if (imageNode == null) return
            const { src, alt, url, href } = imageNode
        },
            checkImage: customCheckImageFn, // 也支持 async 函数
            parseImageSrc: customParseImageSrc, // 也支持 async 函数
        },
        uploadImage:{
            customUpload(file,insertfn){
                var data = new FormData();
                data.append("image", file);
                request({
                    url:"/api/image/uploadimages",
                    method:"post",
                    data:data
                }).then((res) =>{
                    insertfn(res.data.data.url,res.data.data.alt,"使用说明")
                })
            }
        }
        },
    hoverbarKeys:{
        // 'formula': {
        //     menuKeys: ['editFormula',], // “编辑公式”菜单
        // },
        'text':{
            menuKeys:['droppanel']
        },
        'image':{
            menuKeys:['ocr']
        },
    },
}

// 工具栏配置
const toolbarConfig = {
    // toolbarKeys: ['headerSelect', 'bold', 'my-menu-1'],
    insertKeys: {
        index: 0,
        keys: ['save','ocr','droppanel',]
    }
}

// 编辑器实例，必须用 shallowRef ，重要！
const editorRef = shallowRef()

// 内容 HTML
const valueHtml = ref('')
// 编辑器回调函数
const handleCreated = (editor) => {
    
    editorRef.value = editor // 记录 editor 实例，重要！
    if (!editor.getAllMenuKeys()?.includes("insertFormula")) {        
        Boot.registerModule(formulaModule)
    }
    Boot.registerModule(markdownModule)
    editor.setHtml(localStorage.getItem(route.currentRoute.value.query.file_name))
    console.log(localStorage.getItem(route.currentRoute.value.query.file_name))
    // window.editor = editor // 临时测试使用，用完删除
}
const handleChange = (editor) => {
    console.log(editor,getHtml())
    // console.log("change:", editor.children);
    // console.log(editor.children)
}
const handleDestroyed = (editor) => {
    // console.log('destroyed', editor)
}
const handleFocus = (editor) => {
    // console.log('focus', editor)
}
const handleBlur = (editor) => {
    // console.log('blur', editor)
}
const customAlert = (info, type) => {
    // alert(`【自定义提示】${type} - ${info}`)
}
// const customPaste = (editor, event, callback) => {
//     console.log('ClipboardEvent 粘贴事件对象', event)

//     // 自定义插入内容
//     editor.insertText('xxx')

//     // 返回值（注意，vue 事件的返回值，不能用 return）
//     callback(false) // 返回 false ，阻止默认粘贴行为
//     // callback(true) // 返回 true ，继续默认的粘贴行为
// }
// 及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return

    // 销毁，并移除 editor
    editor.destroy()
})
const getHtml = () => {
    const editor = editorRef.value
    if (editor == null) return
}

</script>

<template>
    <div style="border: 1px solid #ccc">
        <!-- 工具栏 -->
        <Toolbar
        :editor="editorRef"
        :defaultConfig="toolbarConfig"
        style="border-bottom: 1px solid #ccc"
        />
        <!-- 编辑器 -->
        <Editor
            v-model="valueHtml"
            :defaultConfig="editorConfig"
            @onChange="handleChange"
            @onCreated="handleCreated"
            @onDestroyed="handleDestroyed"
            @onFocus="handleFocus"
            @onBlur="handleBlur"
            @customAlert="customAlert"
            style="height: 500px"
        />
        
    </div>
    
</template>

<style src="@wangeditor/editor/dist/css/style.css"></style>
<style>
.w-e-panel-my-list {
      text-align: center;
}

.w-e-panel-my-list li {
      display: block;
      cursor: pointer;
      padding: 3px 5px;
}

.w-e-panel-my-list li:hover {
    background-color: #f1f1f1;
}
.EditMain{
    position: relative;
    width:100vw;
    height: 100vh;

    display: grid;
    grid-template-columns: 20% 60% 20%;
  
  }
  .lefttools{
    background-color: rgb(111 118 177 / 60%);
    height: 100%;
    width: 100%;
  }
  .editorcard{
    position: relative;
    width:95%;
    height: 95%;
    left: 2.5%;
    top:2.5%;
    display: grid;
    grid-template-rows: 5% 92% 3%;
    border: 1px solid #4f5c5765;
  }
  .editorcard .editor{
    position: relative;
    width:100%;
    height: 100%;
    left: 0;
    top:0;
    display: grid;
    grid-template-rows: 10% 90%;
  }
  .editorcard .editor{
    position: relative;
    width:100%;
    height: 100%;
    left: 0;
    top:0;
    display: grid;
    grid-template-rows: 10% 90%;
  }
  .toptools{
    background-color: rgba(207, 220, 245, 0.199);
    border-bottom: 1px dashed #9ca19f65;
  }
  .editcont{
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

</style>