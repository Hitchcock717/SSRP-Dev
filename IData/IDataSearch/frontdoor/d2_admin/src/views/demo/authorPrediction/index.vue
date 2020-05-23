<template>
  <d2-container>
    <d2-page-cover>
      <el-button type="primary"
        @click="authorReturn"
        class="button-return">返 回</el-button>
      <el-form :model="textForm" ref="textForm" :rules="rules" label-width="250px" class="demo-textForm">
        <el-form-item label='请选择预测类型' prop="type">
          <el-select v-model="textForm.subject" class='select-item' placeholder="请选择">
            <el-option label="作者性别预测" value="gender"></el-option>
            <el-option label="作者身份预测" value="identity"></el-option>
            <el-option label="作者工作地变更预测" value="hopping"></el-option>
          </el-select>
        </el-form-item>
        <div v-if="textForm.subject=='gender'">
          <el-form-item label="作者姓名">
            <el-input v-model="textForm.authorname" placeholder="请填入作者姓名" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="作者单位">
            <el-input type="textarea" v-model="textForm.authororg" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="作者照片链接">
            <el-input type="textarea" v-model="textForm.authorpic" placeholder="请填入完整url格式" class="col-sm-8"></el-input>
          </el-form-item>
        </div>
        <div v-if="textForm.subject=='identity'">
         <el-form-item label="论文发表数">
            <el-input v-model="textForm.papernumber" placeholder="请填入数字" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="论文引用数">
            <el-input v-model="textForm.papercitation" placeholder="请填入数字" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="H-index">
            <span class="explain">例如:某位作者的H-index值为25, 表明他的论文发表数为25篇并且每篇引用数都大于25次。</span>
            <el-input v-model="textForm.hindex" placeholder="请填入数字" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="G-index">
            <span class="explain">将数篇发表论文按引用数降序排列, G-index表示前g篇的引用数总和至少达到g^2次。</span>
            <el-input v-model="textForm.gindex" placeholder="请填入数字" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="年份范围">
            <span class="explain">作者发表论文年份跨度</span>
            <el-input v-model="textForm.year" placeholder="请填入数字" class="col-sm-8"></el-input>
          </el-form-item>
        </div>
        <div v-if="textForm.subject=='hopping'">
          <el-form-item label="作者单位(可填多个)">
            <el-input type="textarea" v-model="textForm.authororg" placeholder="请填入作者单位(中文逗号分隔)" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="返回预测数">
            <el-input type="textarea" v-model="textForm.ntop" class="col-sm-8"></el-input>
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary"
            @click="authorPrediction()"
            class="button-add">开始预测</el-button>
        </el-form-item>
        <el-form-item>
          <hr/>
        </el-form-item>
      </el-form>
      <el-tabs class="tabs">
        <el-tab-pane label="性别预测" name="gender">
          <el-table :data="genderData">
            <el-table-column prop="name" label="作者姓名判断" align="center">
            </el-table-column>
            <el-table-column prop="search" label="网页搜索判断" align="center">
            </el-table-column>
            <el-table-column prop="face" label="照片识别判断" align="center">
            </el-table-column>
            <el-table-column prop="result" label="最终结果" align="center">
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="身份预测" name="identity">
          <el-table :data="identityData">
            <el-table-column prop="label" label="身份" align="center">
            </el-table-column>
            <el-table-column prop="degree" label="学历" align="center">
            </el-table-column>
            <el-table-column prop="p" label="预测得分" align="center">
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="工作变更预测" name="hopping">
          <el-table :data="hoppingData">
            <el-table-column prop="name" label="跳槽机构" align="center">
            </el-table-column>
            <el-table-column prop="p" label="预测得分" align="center">
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { GenderPrediction } from '@/api/demo/prediction/genderPredictionService'
import { IdentityPrediction } from '@/api/demo/prediction/IdentityPredictionService'
import { HoppingPrediction } from '@/api/demo/prediction/hoppingPredictionService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      genderData: [],
      identityData: [],
      hoppingData: [],
      textForm: {
        subject: '',
        authorname: '',
        authororg: '',
        authorpic: '',
        papernumber: '',
        papercitation: '',
        hindex: '',
        gindex: '',
        year: ''
      },
      rules: {
        subject: [
          { type: 'array', required: true, message: '请至少选择一个领域', trigger: 'change' }
        ],
        authorname: [
          { required: true, message: '请填写作者名称', trigger: 'blur' }
        ],
        authororg: [
          { required: true, message: '请填写作者单位', trigger: 'blur' }
        ],
        authorpic: [
          { required: true, message: '请填写作者照片链接', trigger: 'blur' }
        ],
        papernumber: [
          { required: true, message: '请填写论文发表数', trigger: 'blur' }
        ],
        papercitation: [
          { required: true, message: '请填写论文引用数', trigger: 'blur' }
        ],
        hindex: [
          { required: true, message: '请填写H-index', trigger: 'blur' }
        ],
        gindex: [
          { required: true, message: '请填写G-index', trigger: 'blur' }
        ],
        year: [
          { required: true, message: '请填写年份范围', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    authorReturn () {
      this.$router.push({
        path: '/analysis'
      })
    },
    authorPrediction () {
      console.log(this.textForm.subject)
      if (this.textForm.subject === 'gender') {
        GenderPrediction({
          name: this.textForm.authorname,
          org: this.textForm.authororg,
          image_url: this.textForm.authorpic
        })
          .then(res => {
            var result = res
            if (result !== 'failed') {
              this.genderData = result
              this.$message({
                type: 'success',
                message: '解析成功, 请点击下方tab!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else if (this.textForm.subject === 'identity') {
        IdentityPrediction({
          pc: this.textForm.papernumber,
          cn: this.textForm.papercitation,
          hi: this.textForm.hindex,
          gi: this.textForm.gindex,
          year_range: this.textForm.year
        })
          .then(res => {
            var result = res
            if (result !== 'failed') {
              this.identityData = result
              this.$message({
                type: 'success',
                message: '解析成功, 请点击下方tab!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else {
        HoppingPrediction({
          org_name: this.textForm.authororg,
          ntop: this.textForm.ntop
        })
          .then(res => {
            var result = res
            if (result !== 'failed') {
              this.hoppingData = result
              this.$message({
                type: 'success',
                message: '解析成功, 请点击下方tab!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      }
    }
  }
}
</script>

<style scoped>
 .demo-textForm {
  margin-right: 200px;
  margin-top: 100px;
 }
 .select-item {
  width: 200px;
 }
 .input-with-select {
  width: 500px;
  background-color: #fff;
 }
 .button-return {
  margin-bottom: 30px;
  margin-right: 200px;
  float: right;
 }
</style>
