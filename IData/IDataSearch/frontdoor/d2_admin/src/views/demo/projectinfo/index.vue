<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button type="primary" class="return" @click="submit">返回项目库</el-button>
        <el-table :data="tableData" class="basicinfo"
            style="width: 800px" empty-text="N/A" max-height="550">
          <el-table-column label="项目名称" width="300px" align="center" prop="project"></el-table-column>
          <el-table-column label="创建时间" width="100px" align="center"  prop="date"></el-table-column>
          <el-table-column label="相关领域" width="200px" align="center" prop="type"></el-table-column>
          <el-table-column label="数据来源" width="200px" align="center" prop="source"></el-table-column>
        </el-table>
        <el-table :data="wordData" class="word"
            style="width: 800px" empty-text="N/A" max-height="550">
          <el-table-column label="检索方式" width="100px" align="center" prop="method"></el-table-column>
          <el-table-column label="抽取词汇" width="250px" align="center" prop="extract"></el-table-column>
          <el-table-column label="推荐词汇" width="450px" align="center" prop="recommend"></el-table-column>
        </el-table>
    </d2-page-cover>
  </d2-container>
</template>

<style lang="scss" scoped>
  .return {
    margin-bottom: 15px;
  }
  .word {
    margin-top: 20px;
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetProjectinfo } from '@/api/demo/projectinfo/getprojectinfoService'
export default {
  data () {
    return {
      selectedProject: this.$route.query.selectedProject,
      tableData: [],
      wordData: []
    }
  },
  created () {
    GetProjectinfo({
      name: this.selectedProject
    })
      .then(res => {
        this.result = res
        console.log(this.result)
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '该项目库为空!'
          })
        } else {
          let project = 'project'
          let date = 'date'
          let source = 'source'
          let type = 'type'
          let method = 'method'
          let extract = 'extract'
          let recommend = 'recommend'

          var tableDict1 = { 'project': this.result[project], 'date': this.result[date], 'type': this.result[type], 'source': this.result[source] }
          this.tableData = Array(1).fill(tableDict1)

          var tableDict2 = { 'method': this.result[method], 'extract': this.result[extract], 'recommend': this.result[recommend] }
          this.wordData = Array(1).fill(tableDict2)
        }
      })
  },
  methods: {
    submit () {
      this.$router.push({
        path: '/project'
      })
    }
  }
}
</script>
