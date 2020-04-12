<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="子库名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="子库存储位置" prop="region">
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
        <el-form-item label="领域词表" prop="subrepo">
          <el-button @click="subrepo" type="primary" class="nextpage">浏览</el-button>
        </el-form-item>
        <el-form-item label="选择作者" prop="author">
          <el-select v-model="ruleForm.author" placeholder="请选择作者">
            <el-option
              v-for="item in authors"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              name="method">{{item.label}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择基金" prop="fund">
          <el-select v-model="ruleForm.fund" placeholder="请选择基金">
            <el-option
              v-for="item in funds"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              name="method">{{item.label}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择单位" prop="info">
          <el-select v-model="ruleForm.info" placeholder="请选择单位">
            <el-option
              v-for="item in infos"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              name="method">{{item.label}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择来源" prop="source">
          <el-select v-model="ruleForm.source" placeholder="请选择来源">
            <el-option
              v-for="item in sources"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              name="method">{{item.label}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择发表时间" prop="date">
          <el-date-picker
            v-model="ruleForm.date"
            type="monthrange"
            align="right"
            unlink-panels
            range-separator="至"
            start-placeholder="开始月份"
            end-placeholder="结束月份"
            :picker-options="pickerOptions">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="子库说明" prop="desc">
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
      authors: [{
        value: '选项1',
        label: '刘青'
      }, {
        value: '选项2',
        label: '杨猛'
      }, {
        value: '选项3',
        label: '苏群'
      }, {
        value: '选项4',
        label: '彭迪'
      }],
      funds: [{
        value: '选项1',
        label: '国家自然科学基金项目(批准号:41402031)资助'
      }, {
        value: '选项2',
        label: '国家自然科学基金项目(批准号:41402031)资助'
      }, {
        value: '选项3',
        label: '国家自然科学基金项目(批准号:41402031)资助'
      }, {
        value: '选项4',
        label: '国家自然科学基金项目(批准号:41402031)资助'
      }],
      infos: [{
        value: '选项1',
        label: '北京大学物理学院电子显微镜实验室'
      }, {
        value: '选项2',
        label: '北京大学物理学院电子显微镜实验室'
      }, {
        value: '选项3',
        label: '北京大学物理学院电子显微镜实验室'
      }, {
        value: '选项4',
        label: '北京大学物理学院电子显微镜实验室'
      }],
      sources: [{
        value: '选项1',
        label: '期刊'
      }, {
        value: '选项2',
        label: '期刊'
      }, {
        value: '选项3',
        label: '期刊'
      }, {
        value: '选项4',
        label: '期刊'
      }],
      gettime: this.getTime(),
      pickerOptions: {
        shortcuts: [{
          text: '本月',
          onClick (picker) {
            picker.$emit('pick', [new Date(), new Date()])
          }
        }, {
          text: '今年至今',
          onClick (picker) {
            const end = new Date()
            const start = new Date(new Date().getFullYear(), 0)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近六个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setMonth(start.getMonth() - 6)
            picker.$emit('pick', [start, end])
          }
        }]
      },
      ruleForm: {
        name: 'demo-subrepo',
        desc: 'this is a subrepo for scientific research'
      },
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' },
          { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
        ],
        author: [
          { required: true, message: '请至少选择一位作者', trigger: 'change' }
        ],
        fund: [
          { required: true, message: '请至少选择一项基金', trigger: 'change' }
        ],
        info: [
          { required: true, message: '请至少选择一家单位', trigger: 'change' }
        ],
        source: [
          { required: true, message: '请至少选择一处来源', trigger: 'change' }
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
    subrepo () {
      this.$router.push('/corpusrepo')
    },
    submitForm (ruleForm) {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          this.$router.push('/detailsearch')
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
