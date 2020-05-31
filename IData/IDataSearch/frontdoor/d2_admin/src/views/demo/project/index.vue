<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button
        @click="addProject"
        type="primary"
        class="addProject">添加</el-button>
      <el-table :data="tableData" ref="projectTable"
      style="width: 800px" empty-text="N/A" max-height="600" highlight-current-row @current-change="handleChange">
        <el-table-column label="编号" width="100px" type="index" align="center">
        </el-table-column>
        <el-table-column label="项目库名称" align="center" prop="project">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button @click="setCurrent(scope.row)" type="text" size="small">详情</el-button>
            <el-button size="small" type="text" @click="deleteProject(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .addProject {
    margin-bottom: 15px;
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetProject } from '@/api/demo/project/getprojectService'
import { DeleteProject } from '@/api/demo/project/deleteprojectService'
export default {
  data () {
    return {
      tableData: []
    }
  },
  created () {
    GetProject({})
      .then(res => {
        this.result = res
        console.log(this.result)
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '项目库为空,请添加项目!'
          })
        } else {
          this.tableData = this.result
        }
      })
  },
  methods: {
    addProject () {
      this.$prompt('请输入项目名称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /[\u4e00-\u9fa5_a-zA-Z0-9_]{4,10}/,
        inputErrorMessage: '项目名称长度必须为4-10位'
      }).then(({ value }) => {
        this.$router.push({
          path: '/transition1',
          query: {
            name: value
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        })
      })
    },
    deleteProject (scope) {
      DeleteProject({
        delid: JSON.stringify(scope.row.pk)
      })
        .then(res => {
          var feedback = res
          if (feedback === 'success') {
            this.$message({
              type: 'success',
              message: '删除成功!'
            })
          } else if (feedback === 'failed') {
            this.$message({
              type: 'info',
              message: '删除失败!'
            })
          }
        })

      this.tableData.splice(scope.$index, 1)
    },
    handleChange (val) {
      this.currentRow = val
    },
    setCurrent (row) {
      this.$refs.projectTable.setCurrentRow(row)
      var res = this.currentRow
      console.log(res)
      let project = 'project'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === project && this.tableData[i][key] === res[project]) {
            var selectedProject = this.tableData[i][key] // 数据库id作参数
            this.$router.push({
              path: '/projectinfo',
              query: {
                selectedProject: selectedProject
              }
            })
            console.log(selectedProject)
          }
        }
      }
    }
  }
}
</script>
