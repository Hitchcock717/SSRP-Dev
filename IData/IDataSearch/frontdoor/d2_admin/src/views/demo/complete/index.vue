<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="150px" class="demo-ruleForm">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="创建时间">{{gettime}}</el-form-item>
        <el-form-item label="研究领域" prop="type">
          <el-checkbox-group v-model="ruleForm.type">
            <el-checkbox
              v-for="item in checkList"
              :key="item.label"
              :label="item.label"
              name="type">{{item.label}}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="数据来源" prop="resource">
          <el-checkbox-group v-model="ruleForm.resource">
            <el-checkbox label="知网" name="resource"></el-checkbox>
            <el-checkbox label="维普" name="resource"></el-checkbox>
            <el-checkbox label="万方" name="resource"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="选择自定义词表" prop="corpus">
          <el-select v-model="ruleForm.corpus" placeholder="选择词表">
            <el-option class="corp" v-for="(corp, index) in corpuss" :key="index" :value="corp.repository">{{corp.repository}}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目简介" prop="desc">
          <el-input type="textarea" v-model="ruleForm.desc"></el-input>
        </el-form-item>
        <el-form-item label="搜索方式" prop="method">
          <el-input v-model="ruleForm.method" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="子库名称" prop="subrepo">
          <el-input v-model="ruleForm.subrepo"></el-input>
        </el-form-item>
        <el-form-item label="子库说明" prop="intro">
          <el-input type="textarea" v-model="ruleForm.intro"></el-input>
        </el-form-item>
        <el-form-item label="查看抽取词表" prop="extract">
          <el-select v-model="ruleForm.extract" placeholder="查看抽取词">
            <el-option class="extr" v-for="(extr, index) in extractors" :key="index" :value="extr.originkws">{{extr.originkws}}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="查看推荐词表" prop="recomm">
          <el-select  v-model="ruleForm.recomm" placeholder="查看推荐词">
            <el-option class="recom" v-for="(recom, index) in recommends" :key="index" :value="recom.recommendkws">{{recom.recommendkws}}</el-option>
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
// import { mapState } from 'vuex'
import { AddProject } from '@/api/demo/project/addprojectService'
import { SaveProject } from '@/api/demo/project/saveprojectService'
export default {
  data () {
    return {
      extractors: JSON.parse(this.$route.params.extractors), // 注意解析格式
      recommends: JSON.parse(this.$route.params.recommends),
      corpuss: JSON.parse(this.$route.params.corpus),
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
      options: [],
      gettime: this.getTime(),
      ruleForm: {
        name: '',
        type: [],
        resource: [],
        desc: '',
        method: '',
        extract: '',
        recomm: '',
        subrepo: '',
        intro: '',
        corpus: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' },
          { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
        ],
        subrepo: [
          { required: true, message: '请输入子库名称', trigger: 'blur' },
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
        ],
        intro: [
          { required: true, message: '请填写子库说明', trigger: 'blur' }
        ]
      }
    }
  },
  mounted () {
    var projectName = this.$route.params.name.replace('"', '')
    var newName = projectName.replace('"', '')
    console.log(newName)
    this.ruleForm.name = newName
  },
  beforeRouteEnter (to, from, next) {
    if (from.name === 'recommend') {
      next(vm => {
        vm.ruleForm.method = '论文搜索'
      })
    } else {
      next(vm => {
        vm.ruleForm.method = '词表搜索'
      })
    }
  },
  methods: {
    getTime: function () {
      let yy = new Date().getFullYear()
      let mm = new Date().getMonth() + 1
      let dd = new Date().getDate()
      let hh = new Date().getHours()
      let min = new Date().getMinutes()
      let sec = new Date().getSeconds()
      if (sec < 10) {
        sec = '0' + sec
      }
      let gettime = yy + '-' + mm + '-' + dd + ' ' + hh + ':' + min + ':' + sec
      return gettime
    },
    submitForm (ruleForm) {
      AddProject({
        name: this.ruleForm.name
      })
        .then(res => {
          this.feedback = res
          console.log(this.feedback)
          if (this.feedback !== 'failed') {
            this.$message({
              type: 'success',
              message: '新建项目名称是: ' + this.ruleForm.name
            })
          } else {
            this.$message({
              type: 'info',
              message: '项目名称已存在!'
            })
          }
        })

      console.log(this.ruleForm.corpus)
      SaveProject({
        name: this.ruleForm.name,
        date: this.getTime(),
        type: this.ruleForm.type.join(','),
        source: this.ruleForm.resource.join(','),
        description: this.ruleForm.desc,
        method: this.ruleForm.method,
        extract: JSON.stringify(this.extractors),
        recommend: JSON.stringify(this.recommends),
        corpus: this.ruleForm.corpus,
        subrepo: this.ruleForm.subrepo,
        intro: this.ruleForm.intro
      })
        .then(res => {
          var feedback = res
          if (feedback === 'success') {
            this.$message({
              type: 'success',
              message: '创建成功!'
            })
          } else if (feedback === 'failed') {
            this.$message({
              type: 'info',
              message: '创建失败, 请重试!'
            })
          }
        })
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          this.$router.push({
            name: 'startsearch',
            params: {
              extractors: JSON.stringify(this.extractors),
              recommends: JSON.stringify(this.recommends),
              time: JSON.stringify(this.getTime())
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
 .demo-ruleForm {
    margin-right: 200px;
 }
</style>
