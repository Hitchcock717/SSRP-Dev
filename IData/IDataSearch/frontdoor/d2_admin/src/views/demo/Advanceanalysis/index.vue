<template>
  <d2-container>
    <d2-page-cover>
      <el-button type="primary"
        @click="analyzeReturn"
        class="button-return">返 回</el-button>
      <el-form :model="textForm" ref="textForm" label-width="250px" class="demo-textForm" :class='{fixed:isFixed}'>
        <el-form-item label='请选择分析方式' prop="type">
          <el-select v-model="textForm.subject" class='select-item' placeholder="请选择">
            <el-option label="高频词" value="frequency"></el-option>
            <el-option label="期刊发文量" value="volume"></el-option>
            <el-option label="词间关系" value="relation"></el-option>
            <el-option label="论文主题模型" value="model"></el-option>
            <el-option label="情感分析" value="emotion"></el-option>
          </el-select>
        </el-form-item>
        <div v-if="textForm.subject=='frequency'">
          <el-form-item label="数据来源">
            <el-select v-model="textForm.source" class='select-item' placeholder="请选择来源">
              <el-option class="file" v-for="(file, index) in filerepos" :key="index" :value="file.name">{{file.name}}</el-option>
            </el-select>
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary"
            @click="Analyze()"
            :disabled="!textForm.subject"
            class="button-add">开始分析</el-button>
        </el-form-item>
        <el-form-item>
          <hr/>
        </el-form-item>
        <el-tabs>
          <el-tab-pane label="标题高频词" name="title">
            <ve-wordcloud :data="titleData"></ve-wordcloud>
          </el-tab-pane>
          <el-tab-pane label="关键词高频词" name="kws">
            <ve-wordcloud :data="kwsData"></ve-wordcloud>
          </el-tab-pane>
          <el-tab-pane label="摘要高频词" name="abstract">
            <ve-wordcloud :data="abstractData"></ve-wordcloud>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { FrequencyAnalyze } from '@/api/demo/analysis/frequencyService'
import { AITitlePrediction } from '@/api/demo/prediction/AItitlePredictionService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      filerepos: JSON.parse(this.$route.params.file),
      isFixed: '',
      textForm: {
        subject: '',
        source: ''
      },
      titleData: [],
      kwsData: [],
      abstractData: []
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
    analyzeReturn () {
      this.$router.push({
        path: '/analysis'
      })
    },
    Analyze () {
      if (this.textForm.subject === 'frequency') {
        FrequencyAnalyze({
          source: this.textForm.source
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
