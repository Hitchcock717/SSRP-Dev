<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-steps :active="2" class="process" space="20%" align-center="true">
        <el-step title="选择检索方式" description="请选择输入论文信息检索或上传词表搜索"></el-step>
        <el-step title="准备检索" description="请按提示输入检索信息或上传格式正确的词表"></el-step>
        <el-step title="完成项目创建" description="项目信息保存完毕"></el-step>
        <el-step title="创建子库" description="获取更有价值的数据并分析"></el-step>
        <el-step title="完成子库创建" description="子库信息保存完毕"></el-step>
      </el-steps>
      <el-form :model="uploadForm" enctype="multipart/form-data" class="demo-uploadForm">
        <el-form-item label="上传词表文件">
          <el-upload
            action="http://127.0.0.1:8000/api/mockupload/"
            ref="upload"
            drag
            multiple
            accept=".txt"
            :limit="1"
            :on-change="handleChange"
            :on-exceed="handleExceed"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">只能上传txt文件(utf-8编码)，且不超过5mb</div>
          </el-upload>
          <el-button size="default" @click="submit(file)"  type="primary" class="button-save">保存</el-button>
        </el-form-item>
        <el-form-item>
          <el-input
            type="textarea"
            autosize
            v-model="uploadForm.textarea"></el-input>
          <el-button size="default" @click="view" type="primary" class="button-view">显示</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { ParseUpload } from '@/api/demo/uploadService'
export default {
  data () {
    return {
      uploadForm: {
        textarea: ''
      },
      name: ''
    }
  },
  methods: {
    handleChange (file, fileList) {
      let reader = new FileReader()
      if (file.raw) {
        var uploadName = file.raw.name
        localStorage.setItem('name', uploadName)
        console.log(uploadName)

        reader.readAsText(file.raw, 'utf-8')
        reader.onload = function (e) {
          var contentHtml = e.target.result
          localStorage.setItem('content', contentHtml)
          console.log(contentHtml)
        }
      }
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning('当前限制选择 1 个文件，本次选择文件数量过多！')
    },
    beforeRemove (file, fileList) {
      this.uploadForm.textarea = ''
      return this.$confirm('确定移除此文件？')
    },
    view () {
      if (localStorage.getItem('content')) {
        this.uploadForm.textarea = localStorage.getItem('content')
        console.log(this.uploadForm.textarea)
        // localStorage.removeItem('content')
      } else {
        this.$message({
          type: 'info',
          message: '无可显示内容!'
        })
      }
    },
    submit (file) {
      if (localStorage.getItem('content')) {
        ParseUpload({
          content: localStorage.getItem('content'),
          name: localStorage.getItem('name')
        })
          .then(res => {
            this.feedback = res
            console.log(this.feedback[0])
            if (this.feedback !== 'failed') {
              this.$message({
                type: 'success',
                message: '词表解析成功!'
              })
              localStorage.removeItem('content')
              localStorage.removeItem('name')

              var results = JSON.stringify(this.feedback)
              localStorage.setItem('results', results)

              this.$router.push({
                path: '/recommend2',
                query: {
                  name: this.$route.query.name
                }
              })
            } else {
              this.$message({
                type: 'info',
                message: '词表解析错误, 请重新上传!'
              })
              localStorage.removeItem('content')
              localStorage.removeItem('name')
            }
          })
      } else {
        this.$message({
          type: 'info',
          message: '请上传文件!'
        })
      }
    }
  }
}
</script>

<style scoped>
  .button-save {
    float: right;
  }
  .demo-uploadForm {
    margin-left: 150px;
  }
  .button-view {
    margin-top: 15px;
    float: right;
  }
  .process {
    margin-bottom: 80px;
  }
</style>
