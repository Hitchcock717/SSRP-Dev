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
        <el-form-item label="开启子库" prop="subrepo">
          <el-switch v-model="ruleForm.subrepo" :disabled="true"></el-switch>
        </el-form-item>
        <el-form-item label="研究领域" prop="type">
          <el-checkbox-group v-model="ruleForm.type" :disabled="true">
            <el-checkbox
              v-for="item in checkList"
              :key="item"
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
        <el-form-item label="搜索词表" prop="list">
          <el-input type="textarea" v-model="ruleForm.list" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">完成创建</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import D2PageCover from './components/d2-page-cover'
export default {
  components: {
    D2PageCover
  },
  data () {
    return {
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
        list: '脑膜瘤, 免疫组化, 电镜'
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
          this.$router.push('/notice1')
          // alert('创建成功!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>
