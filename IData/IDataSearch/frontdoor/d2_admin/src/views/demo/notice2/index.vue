<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-steps :active="5" class="process" space="20%" align-center=true>
        <el-step title="选择检索方式" description="请选择输入论文信息检索或上传词表搜索"></el-step>
        <el-step title="准备检索" description="请按提示输入检索信息或上传格式正确的词表"></el-step>
        <el-step title="完成项目创建" description="项目信息保存完毕"></el-step>
        <el-step title="创建子库" description="获取更有价值的数据并分析"></el-step>
        <el-step title="完成子库创建" description="子库信息保存完毕"></el-step>
      </el-steps>
      <div class="block">
        <el-timeline>
          <el-timeline-item type="success" placement="top">
            <el-card>
              <i slot="prepend" class="el-icon-success"></i>
              <h4>子库创建成功</h4>
            </el-card>
          </el-timeline-item>
          <el-timeline-item type="success" placement="top">
            <el-card>
              <h4>搜索完成</h4>
              <h4>下方为搜索结果汇总统计表, 点击确定按钮进入详细结果列表</h4>
              <p nowrap>搜索结果提交时间为: {{ gettime }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
      <el-table :data="tableData" class="result" style="width: 600px" empty-text="N/A" max-height="550">
        <el-table-column prop="query" label="高级检索表达式" width="400px" align="center">
        </el-table-column>
        <el-table-column prop="raw_count" label="过滤前搜索结果数" width="100px" align="center">
        </el-table-column>
        <el-table-column prop="filter_search_count" label="过滤后搜索结果数" width="100px" align="center">
        </el-table-column>
      </el-table>
      <el-button size="default" @click="submit" type="primary" class="confirm">确 定</el-button>
    </d2-page-cover>
  </d2-container>
</template>

<script>
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      result: JSON.parse(this.$route.query.result),
      tableData: [],
      gettime: this.getTime()
    }
  },
  mounted () {
    let query = 'query'
    let raw = 'raw_count'
    let filter = 'filter_search_count'
    var tableDict1 = { 'query': JSON.stringify(this.result[query]), 'raw_count': this.result[raw], 'filter_search_count': this.result[filter] }
    this.tableData = Array(1).fill(tableDict1)
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
    submit () {
      this.$router.push({
        path: '/detailsearch'
      })
    }
  }
}
</script>

<style scoped>
  .block {
    width: 600px;
  }
  .confirm {
    float: right;
    margin-top: 20px;
    margin-right: 30px;
  }
  .process {
    margin-bottom: 20px;
  }
</style>
