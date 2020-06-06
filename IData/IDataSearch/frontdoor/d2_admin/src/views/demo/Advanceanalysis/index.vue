<template>
  <d2-container>
    <d2-page-cover>
      <el-form :model="textForm" ref="textForm" label-width="250px" class="demo-textForm" :class='{fixed:isFixed}'>
        <el-form-item label='返回入口'>
          <el-button type="primary"
            @click="analyzeReturn"
            class="button-return">返 回</el-button>
        </el-form-item>
        <el-form-item label='请选择分析方式'>
          <el-select v-model="textForm.subject" class='select-item' placeholder="请选择">
            <el-option label="高频词" value="frequency"></el-option>
            <el-option label="期刊发文量" value="volume"></el-option>
            <el-option label="词间关系" value="relation"></el-option>
            <el-option label="主题分布" value="classify"></el-option>
            <el-option label="作者合作关系" value="cooperation"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据来源">
            <el-select v-model="textForm.source" class='select-item' placeholder="请选择来源">
              <el-option class="file" v-for="(file, index) in filerepos" :key="index" :value="file.name">{{file.name}}</el-option>
            </el-select>
        </el-form-item>
        <div v-if="textForm.subject=='classify'">
          <el-form-item label="自定义主题数">
            <el-select v-model="textForm.theme" class='select-theme' placeholder="请选择">
              <el-option label="1" value="1"></el-option>
              <el-option label="2" value="2"></el-option>
              <el-option label="3" value="3"></el-option>
              <el-option label="4" value="4"></el-option>
              <el-option label="5" value="5"></el-option>
              <el-option label="6" value="6"></el-option>
              <el-option label="7" value="7"></el-option>
              <el-option label="8" value="8"></el-option>
              <el-option label="9" value="9"></el-option>
              <el-option label="10" value="10"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="自定义主题词数">
            <el-select v-model="textForm.themeword" class='select-themeword' placeholder="请选择">
              <el-option label="5" value="5"></el-option>
              <el-option label="10" value="10"></el-option>
              <el-option label="15" value="15"></el-option>
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
        <el-form-item label="启动分析">
          <el-button type="primary"
            @click="Analyze()"
            :disabled="!textForm.subject"
            class="button-add">分 析</el-button>
        </el-form-item>
        <div v-if="textForm.subject=='relation'">
          <el-form-item label="启动绘制">
            <el-button type="primary"
              @click="create()"
              :disabled="!textForm.subject"
              class="button-vis">显 示</el-button>
          </el-form-item>
        </div>
        <div v-if="textForm.subject=='cooperation'">
          <el-form-item label="启动绘制">
            <el-button type="primary"
              @click="create2()"
              :disabled="!textForm.subject"
              class="button-vis">显 示</el-button>
          </el-form-item>
        </div>
        <el-form-item>
          <hr/>
        </el-form-item>
      </el-form>
      <div class="block1" v-if="textForm.subject=='frequency'">
        <d2-text-center>标题高频词词云图</d2-text-center>
        <ve-wordcloud :data="titleData"></ve-wordcloud>
        <d2-text-center>关键词高频词词云图</d2-text-center>
        <ve-wordcloud :data="kwsData"></ve-wordcloud>
        <d2-text-center>摘要高频词词云图</d2-text-center>
        <ve-wordcloud :data="abstractData"></ve-wordcloud>
      </div>
      <div class="block2" v-if="textForm.subject=='volume'">
        <d2-text-center>期刊发文量饼图</d2-text-center>
        <ve-pie :data="volumeData"></ve-pie>
      </div>
      <div class="block3" v-if="textForm.subject=='relation'">
        <div id="visualization" class="network"></div>
      </div>
      <div class="block4" v-if="textForm.subject=='classify'">
        <div v-for="(item, index) in chartList" :key="index" class="classify">
          <d2-text-center>主题序号: {{ index + 1 }}</d2-text-center>
          <ve-bar :data="item"></ve-bar>
        </div>
      </div>
      <div class="block5" v-if="textForm.subject=='cooperation'">
        <div id="cooperation" class="cooperation"></div>
      </div>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { DataSet, Network } from 'vis/index-network'
import { FrequencyAnalyze } from '@/api/demo/analysis/frequencyService'
import { VolumeAnalyze } from '@/api/demo/analysis/volumeService'
import { RelationAnalyze } from '@/api/demo/analysis/relationService'
import { ClassifyAnalyze } from '@/api/demo/analysis/classifyService'
import { CooperationAnalyze } from '@/api/demo/analysis/cooperationService'
import 'v-charts/lib/style.css'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      filerepos: JSON.parse(this.$route.params.file),
      chartList: [],
      isFixed: '',
      network: null,
      textForm: {
        subject: '',
        source: '',
        date: '',
        theme: '',
        themeword: ''
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
      }
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
    create () {
      // create an array with nodes
      var nodes = new DataSet(this.nodes)

      // create an array with edges
      var edges = new DataSet(this.edges)

      // create a network
      var container = document.querySelector('#visualization')

      // provide the data in the vis format
      var data = {
        nodes: nodes,
        edges: edges
      }
      var options = {}

      // initialize your network!
      this.network = new Network(container, data, options)
    },
    create2 () {
      // create an array with nodes
      var nodes = new DataSet(this.nodes2)

      // create an array with edges
      var edges = new DataSet(this.edges2)

      // create a network
      var container = document.querySelector('#cooperation')

      // provide the data in the vis format
      var data = {
        nodes: nodes,
        edges: edges
      }
      var options = {}

      // initialize your network!
      this.network = new Network(container, data, options)
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
              this.$message({
                type: 'success',
                message: '解析成功!'
              })
              let kws = 'kws'
              let title = 'title'
              let abstract = 'abstract'
              this.titleData.rows = result[title]
              this.kwsData.rows = result[kws]
              this.abstractData.rows = result[abstract]
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else if (this.textForm.subject === 'volume') {
        var pubDate = this.textForm.date
        var startDate = JSON.stringify(pubDate[0]).substring(1, 11)
        var endDate = JSON.stringify(pubDate[1]).substring(1, 11)
        console.log(startDate)
        console.log(endDate)
        VolumeAnalyze({
          start: startDate,
          end: endDate,
          source: this.textForm.source
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              this.volumeData.rows = result
              this.$message({
                type: 'success',
                message: '解析成功!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else if (this.textForm.subject === 'relation') {
        RelationAnalyze({
          source: this.textForm.source
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              let nodes = 'nodes'
              let edges = 'edges'
              this.nodes = result[nodes]
              this.edges = result[edges]
              this.$message({
                type: 'success',
                message: '解析成功!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else if (this.textForm.subject === 'classify') {
        ClassifyAnalyze({
          source: this.textForm.source,
          theme: this.textForm.theme,
          themeword: this.textForm.themeword
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              this.chartList = result
              this.$message({
                type: 'success',
                message: '解析成功!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else if (this.textForm.subject === 'cooperation') {
        CooperationAnalyze({
          source: this.textForm.source
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              let nodes = 'nodes'
              let edges = 'edges'
              this.nodes2 = result[nodes]
              this.edges2 = result[edges]
              this.$message({
                type: 'success',
                message: '解析成功!'
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
  margin-right: 100px;
  margin-top: 100px;
 }
 .select-item {
  width: 300px;
 }
 .input-with-select {
  width: 500px;
  background-color: #fff;
 }
 .visualization {
  width: 800px;
  height: 600px;
 }
 .cooperation {
  width: 800px;
  height: 600px;
 }
 .classify {
  width: 800px;
 }
 .network {
  height: 400px;
  width: 800px;
 }
</style>
