<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="存储位置" prop="region">
          <el-upload
            class="upload"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="fileList">
            <el-button size=”small“ type="primary">浏览</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="创建时间" required>{{gettime}}</el-form-item>
        <el-form-item label="研究领域" prop="type">
          <el-checkbox-group v-model="ruleForm.type">
            <el-checkbox label="基础科学" name="type"></el-checkbox>
            <el-checkbox label="工程技术" name="type"></el-checkbox>
            <el-checkbox label="医学" name="type"></el-checkbox>
            <el-checkbox label="农林" name="type"></el-checkbox>
            <el-checkbox label="社会科学" name="type"></el-checkbox>
            <el-checkbox label="其他" name="type"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="数据来源" prop="resource">
          <el-checkbox-group v-model="ruleForm.resource">
            <el-checkbox label="知网" name="resource"></el-checkbox>
            <el-checkbox label="维普" name="resource"></el-checkbox>
            <el-checkbox label="万方" name="resource"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="项目简介" prop="desc">
          <el-input type="textarea" v-model="ruleForm.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
export default {
  data () {
    return {
      fileList: [
        {
          name: 'test',
          url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        }
      ],
      gettime: this.getTime(),
      ruleForm: {
        name: 'demo',
        region: '',
        subrepo: true,
        type: ['基础科学'],
        resource: ['知网'],
        desc: 'this is for scientific research'
      },
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' },
          { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
        ],
        type: [
          { type: 'array', required: true, message: '请至少选择一个领域', trigger: 'change' }
        ],
        resource: [
          { type: 'array', required: true, message: '请至少选择一处数据来源', trigger: 'change' }
        ],
        desc: [
          { required: true, message: '请填写项目简介', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning('当前限制选择1个文件')
    },
    beforeRemove (file, fileList) {
      return this.$confirm('确定移除 $(file.name}?')
    },
    getTime: function () {
      // var _this = this
      let yy = new Date().getFullYear()
      let mm = new Date().getMonth() + 1
      let dd = new Date().getDate()
      let gettime = yy + '-' + mm + '-' + dd
      return gettime
    },
    submitForm (ruleForm) {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          this.$router.push('/transition1')
          // alert('创建成功!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (ruleForm) {
      this.$refs.ruleForm.resetFields()
    }
  }
}
</script>
