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
        <div v-if="textForm.subject=='volume'">
          <el-form-item label="选择日期范围">
            <el-date-picker
              v-model="textForm.date"
              type="daterange"
              align="right"
              unlink-panels
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :picker-options="pickerOptions">
            </el-date-picker>
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
          <el-tab-pane label="期刊发文量" name="volume">
            <ve-pie :data="volumeData"></ve-pie>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { FrequencyAnalyze } from '@/api/demo/analysis/frequencyService'
import { VolumeAnalyze } from '@/api/demo/analysis/volumeService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      filerepos: JSON.parse(this.$route.params.file),
      isFixed: '',
      textForm: {
        subject: '',
        source: '',
        date: ''
      },
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      },

      titleData: {
        columns: ['word', 'count'],
        rows: []
      },
      kwsData: {
        columns: ['word', 'count'],
        rows: []
      },
      abstractData: {
        columns: ['word', 'count'],
        rows: []
      },
      volumeData: {
        columns: ['word', 'count'],
        rows: []
      },
      loading: true
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
              let kws = 'kws'
              let title = 'title'
              let abstract = 'abstract'
              this.titleData.rows = result[title]
              this.kwsData.rows = result[kws]
              this.abstractData.rows = result[abstract]
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
        var pubDate = this.textForm.date
        var startDate = JSON.stringify(pubDate[0]).substring(1, 11)
        var endDate = JSON.stringify(pubDate[1]).substring(1, 11)
        console.log(startDate)
        console.log(endDate)
        VolumeAnalyze({
          start: startDate,
          end: endDate
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              this.volumeData.rows = result
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
  width: 300px;
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
