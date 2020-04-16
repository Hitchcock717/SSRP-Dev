<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="ruleForm.name" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="存储位置" prop="region">
          <el-upload
            :disabled="true"
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
          <el-checkbox-group v-model="ruleForm.type" :disabled="true">
            <el-checkbox
              v-for="item in checkList"
              :key="item.label"
              :label="item.label"
              name="type">{{item.label}}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="数据来源" prop="resource">
          <el-checkbox-group v-model="ruleForm.resource" :disabled="true">
            <el-checkbox label="知网" name="resource"></el-checkbox>
            <el-checkbox label="维普" name="resource"></el-checkbox>
            <el-checkbox label="万方" name="resource"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="项目简介" prop="desc">
          <el-input type="textarea" v-model="ruleForm.desc" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="搜索方式" prop="method">
          <el-select v-model="ruleForm.method" :disabled="true">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              name="method">{{item.label}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="抽取词表" prop="extract_list">
          <el-select v-model="ruleForm.extract" placeholder="查看抽取词">
            <el-option class="extr" v-for="(extr, index) in extractors" :key="index.value" :label="index.label"
              :value="index.value">抽取词: {{extr.originkws}}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="推荐词表" prop="recomm_list">
          <el-select  v-model="ruleForm.recomm" placeholder="查看推荐词">
            <el-option class="recom" v-for="(recom, index) in recommends" :key="index.value" :label="index.label"
              :value="index.value">推荐词: {{recom.recommendkws}}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">完成创建</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
export default {
  data () {
    return {
      extractors: this.$route.query.extractors,
      recommends: this.$route.query.recommends,
      fileList: [
        {
          name: 'example',
          url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        }
      ],
      checkList: [
        {
          label: '基础科学'
        },
        {
          label: '工程技术'
        },
        {
          label: '农林'
        },
        {
          label: '社会科学'
        },
        {
          label: '医学'
        },
        {
          label: '其他'
        }
      ],
      options: [{
        value: '选项1',
        label: '关键词搜索'
      }, {
        value: '选项2',
        label: '标题搜索'
      }, {
        value: '选项3',
        label: '词表搜索'
      }],
      gettime: this.getTime(),
      ruleForm: {
        name: 'demo',
        region: '',
        subrepo: true,
        type: ['基础科学'],
        resource: ['知网'],
        desc: 'this is for scientific research',
        method: '标题搜索',
        extract: '',
        recomm: ''
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
          this.$router.push({
            path: '/startsearch',
            query: {
              extractors: JSON.stringify(this.extractors),
              recommends: JSON.stringify(this.recommends)
            }
          })
          console.log(JSON.stringify(this.extractors))
          // alert('创建成功!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  },
  created () {
    // this.extractors = window.localStorage.getItem('extractors')
    // console.log(this.extractors)
    // this.recommends = window.localStorage.getItem('recommends')
  }
}
</script>
