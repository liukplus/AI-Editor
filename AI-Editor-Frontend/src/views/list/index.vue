<template>
  <div>
  <el-button class="mt-4" style="width: 100%" type="primary" @click="displayForm=true">
    新建
  </el-button>
  <el-table :data="filterTableData" style="width: 99.97%;--el-table-border-color: none;"
            :highlight-current-row="false"
            :header-cell-style="{ backgroundColor: 'black', color: '#ffffff', fontSize: '14px', textAlign: 'center'}"
            :cell-style="{ color: '#fff', fontSize: '14px', textAlign: 'center'}"
            :row-style="{ color: '#fff', fontSize: '14px', textAlign: 'center', }" :row-class-name="tableRowClassName"
            empty-text="暂无数据" max-height="818">
    <el-table-column prop="text_name" label="文件名" width="300" sortable />
    <el-table-column prop="description" label="描述" width="300" />
    <el-table-column fixed="right" label="Operations" min-width="120">
      <template #header>
        <el-input v-model="search" size="small" placeholder="Type to search" />
      </template>
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          Edit
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
        >
          Delete
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  
  <el-dialog
    v-model="displayForm"
    title="Tips"
    width="500"
    :before-close="handleClose"
  >
  <el-form ref="ruleFormRef" :rules="rules" :model="form" label-width="auto" style="max-width: 600px">
    <el-form-item label="文件名" prop="text_name">
      <el-input v-model="form.text_name" />
    </el-form-item>
    <el-form-item label="文件描述" prop="description">
      <el-input v-model="form.description" />
    </el-form-item>
  </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="displayForm = false">Cancel</el-button>
        <el-button type="primary" @click="onSubmit(ruleFormRef)">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
  
</div>
</template>

<script lang="ts" setup>
// import axios from 'axios';
import router, { Layout } from "@/router";
import request from "@/utils/myrequest"
import path from "path";
import type { FormInstance, FormRules } from 'element-plus'

const ruleFormRef = ref<FormInstance>()
interface FileItem {
  text_name: string
  description: string
}
var displayForm = ref(false)
var form = reactive({
  text_name:"",
  description:"",
})
var tableData = ref([])

const handleClose = (done: () => void) => {
  // ElMessageBox.confirm('Are you sure to close this dialog?')
  //   .then(() => {
      done()
    // })
    // .catch(() => {
    //   // catch error
    // })
}
const checkTextName = (rule: any, value: any, callback: any) => {
  console.log("checkTextName called")
  if (!value || value=="") {
    return callback(new Error('请输入文件名'))
  }
  setTimeout(() => {
    tableData.value.forEach((f)=>{
      console.log(f.text_name)
      if (f.text_name == value){
        callback(new Error("文件名重复"))
      }
    })
    callback()
  }, 1000)
}

const rules = reactive<FormRules<typeof form>>({text_name: [{validator:checkTextName,trigger:'blur'},],})
onBeforeMount(() => {
  console.log(router.getRoutes())
  const form = new FormData()
  request({
    method: 'post',
    url:"/api/richtext/get_richtext_list",
    data:form,
  }).then(
    (res) => {
      tableData.value.unshift(...res.data.data)
      res.data.data.forEach((val: string,_: any) => {
        createRoute(val.text_name)
      })
    }
  )
})
const onSubmit = (formEl:FormInstance|undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      displayForm.value = false
      tableData.value.push(form)
      var formData = new FormData()
      formData.append("text_name",form.text_name)
      formData.append("content","")
      request({
        method: 'post',
        url:"/api/richtext/upload_richtext",
        data:formData,
      }).then(
        (res) => {
          createRoute(form.text_name)
          var x = form.text_name
          form = reactive({
            text_name:"",
            description:"",
          })
          router.push("/file/"+x,x)
        }
      )
    } else {
      console.log('error submit!')
    }
  })
  
}
const createRoute = (filename : string) => {
  router.addRoute({path:"/file",
  component: Layout,
  redirect: "/file"+filename,
  children:[
    {
      path:filename,
      component:() => import("@/views/editor/ExtendedEditor.vue"),
      meta:{hidden:true,title:filename},
      props: router => ({query:router.query.text_name})
    }
  ]})
}
const search = ref('')
const filterTableData = computed(() =>
  tableData.value.filter(
    (data) =>
      !search.value ||
      data.text_name.toLowerCase().includes(search.value.toLowerCase())
  )
)
const handleEdit = (index: number, row: FileItem) => {
  console.log(index, row)
  if (localStorage.getItem(row.text_name)==null){
    const form = new FormData()
    form.append("text_id",row.text_name)
    request({
      method:"post",
      url:"/api/richtext/get_richtext",
      data:form
    }).then((res) => 
    {
      localStorage.setItem(row.text_name,res.data.data)
      console.log(res.data.data)
    })
  }
  console.log(router.getRoutes())
  router.push("/file/"+row.text_name,row.text_name)
}
const handleDelete = (index: number, row: FileItem) => {
  console.log(index, row)
}
</script>
<style lang="scss" scoped>

</style>
