<template>
  <d2-container>
    <d2-page-cover>
      <el-button type="primary"
        @click="titleReturn"
        class="button-return">返 回</el-button>
      <el-form :model="textForm" ref="textForm" label-width="250px" class="demo-textForm" :class='{fixed:isFixed}'>
        <el-form-item label='请选择预测领域' prop="type">
          <el-select v-model="textForm.subject" class='select-item' placeholder="请选择">
            <el-option label="一般领域" value="一般领域"></el-option>
            <el-option label="AI领域" value="AI领域"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label='请输入预测信息' prop="text">
          <el-input placeholder="AI领域请输入关键词(中文逗号分隔), 否则输入标题" v-model="textForm.body" class="input-with-select" @keyup.enter.native="titlePrediction()">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary"
            @click="titlePrediction()"
            :disabled="!textForm.subject || !textForm.body"
            class="button-add">开始预测</el-button>
        </el-form-item>
        <el-form-item>
          <hr/>
        </el-form-item>
        <el-form-item>
          <el-tabs>
            <el-tab-pane label="一般领域" name="common">
              <el-table :data="tableData">
                <el-table-column prop="group" label="类别" width="80" align="center">
                </el-table-column>
                <el-table-column prop="name" label="所属领域" width="200">
                </el-table-column>
                <el-table-column prop="p" label="预测得分">
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="AI领域" name="ai">
              <el-table :data="AIData">
                <el-table-column prop="group" label="类别" width="80" align="center">
                </el-table-column>
                <el-table-column prop="name" label="所属领域" width="200">
                </el-table-column>
                <el-table-column prop="p" label="预测得分">
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { TitlePrediction } from '@/api/demo/prediction/titlePredictionService'
import { AITitlePrediction } from '@/api/demo/prediction/AItitlePredictionService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      isFixed: '',
      textForm: {
        subject: '',
        body: ''
      },
      tableData: [],
      AIData: []
    }
  },
  methods: {
    onScroll () {
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
      var offsetTop = this.$refs.wordForm.offsetTop
      console.log('scrollTop:' + scrollTop + 'offsetTop:' + offsetTop)
      if (scrollTop > offsetTop) {
        this.isFixed = true
      } else {
        this.isFixed = false
      }
    },
    titleReturn () {
      this.$router.push({
        path: '/analysis'
      })
    },
    titlePrediction () {
      // var titleArray = this.textForm.body.split()
      // console.log(titleArray)
      if (this.textForm.subject === '一般领域') {
        TitlePrediction({
          titles: this.textForm.body
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              this.tableData = result
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
        AITitlePrediction({
          words: this.textForm.body
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              this.AIData = result
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
  },
  created () {
    window.addEventListener('scroll', this.onScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style scoped>
 .demo-textForm {
  margin-right: 200px;
  margin-top: 100px;
 }
 .select-item {
  width: 150px;
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
