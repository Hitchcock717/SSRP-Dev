<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" style="width: 500px" label-width="150px" class="demo-ruleForm">
        <el-form-item label="姓名" prop="name">
          <el-input type="text" v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="ruleForm.gender">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input type="text" v-model="ruleForm.age"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="mail">
          <el-input type="text" v-model="ruleForm.mail"></el-input>
        </el-form-item>
        <el-form-item label="研究方向" prop="job">
          <el-input type="text" v-model="ruleForm.job"></el-input>
        </el-form-item>
        <el-form-item label="工作单位" prop="place">
          <el-input type="text" v-model="ruleForm.place"></el-input>
        </el-form-item>
        <el-form-item label="个性签名" prop="sign">
          <el-input type="textarea" v-model="ruleForm.sign"></el-input>
        </el-form-item>
        <el-form-item label="邮件推送(默认)" prop="post">
          <el-switch v-model="ruleForm.post" active-color="#13ce66" inactive-color="#ff4949" disabled></el-switch>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { SavePersonal } from '@/api/demo/personal/savepersonalService'
import { GetPersonal } from '@/api/demo/personal/getpersonalService'
import { validateEmail } from '@/api/demo/validateService'
export default {
  data () {
    return {
      ruleForm: {
        name: '',
        gender: '',
        age: '',
        mail: '',
        job: '',
        place: '',
        post: true,
        sign: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        mail: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ],
        job: [
          { required: true, message: '请填写研究方向', trigger: 'blur' }
        ],
        place: [
          { required: true, message: '请输入工作单位', trigger: 'blur' }
        ],
        sign: [
          { required: true, message: '请填写个人签名', trigger: 'blur' }
        ]
      }
    }
  },
  mounted () {
    GetPersonal({})
      .then(res => {
        this.result = res
        console.log(this.result)
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '请完善个人信息!'
          })
        } else {
          let name = 'name'
          let gender = 'gender'
          let age = 'age'
          let email = 'email'
          let job = 'job'
          let place = 'place'
          let post = 'post'
          let sign = 'sign'
          this.ruleForm.name = this.result[name]
          this.ruleForm.gender = this.result[gender]
          this.ruleForm.age = this.result[age]
          this.ruleForm.mail = this.result[email]
          this.ruleForm.job = this.result[job]
          this.ruleForm.place = this.result[place]
          this.ruleForm.post = Boolean(this.result[post])
          this.ruleForm.sign = this.result[sign]
        }
      })
  },
  methods: {
    submitForm (ruleForm) {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          SavePersonal({
            name: this.ruleForm.name,
            gender: this.ruleForm.gender,
            age: this.ruleForm.age,
            email: this.ruleForm.mail,
            job: this.ruleForm.job,
            place: this.ruleForm.place,
            post: String(this.ruleForm.post),
            sign: this.ruleForm.sign
          })
            .then(res => {
              var feedback = res
              if (feedback === 'success') {
                this.$message({
                  type: 'success',
                  message: '个人信息保存成功!'
                })
              } else if (feedback === 'failed') {
                this.$message({
                  type: 'info',
                  message: '个人信息未修改!'
                })
              }
              this.$router.push({
                path: '/index'
              })
            })
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

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
