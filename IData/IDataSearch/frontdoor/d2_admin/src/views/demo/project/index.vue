<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button
        @click="addProject"
        type="primary"
        class="addProject">添加</el-button>
      <el-button type="primary"
        @click="subrepo"
        class="subrepo">查看子库目录</el-button>
      <el-button type="primary"
        @click="corpus"
        class="corpus">查看自定义词表</el-button>
      <el-table :data="pendData" ref="pendTable"
      style="width: 800px" empty-text="N/A" max-height="600" highlight-current-row @current-change="handleChange1">
        <el-table-column label="编号" width="100px" type="index" align="center">
        </el-table-column>
        <el-table-column label="待办项目名称" align="center" prop="project">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button @click="setCurrent1(scope.row)" type="text" size="small">详情</el-button>
            <el-button size="small" type="text" @click="deletePending(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-table :data="tableData" ref="projectTable" class="project"
      style="width: 800px" empty-text="N/A" max-height="600" highlight-current-row @current-change="handleChange2">
        <el-table-column label="编号" width="100px" type="index" align="center">
        </el-table-column>
        <el-table-column label="全部项目名称" align="center" prop="project">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button @click="setCurrent2(scope.row)" type="text" size="small">详情</el-button>
            <el-button size="small" type="text" @click="deleteProject(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .addProject {
    margin-left: 15px;
    margin-bottom: 15px;
  }
  .subrepo {
    margin-left: 15px;
    margin-bottom: 15px;
  }
  .corpus {
    margin-bottom: 15px;
  }
  .project {
    margin-top: 30px;
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetProject } from '@/api/demo/project/getprojectService'
import { GetPending } from '@/api/demo/pending/getpendingService'
import { DeletePending } from '@/api/demo/pending/deletependingService'
import { DeleteProject } from '@/api/demo/project/deleteprojectService'
export default {
  data () {
    return {
      tableData: [],
      pendData: []
    }
  },
  created () {
    GetPending({})
      .then(res => {
        this.result1 = res
        if (this.result1 === 'failed') {
          console.log('待办项目为空')
        } else {
          this.pendData = this.result1
        }
      })
    GetProject({})
      .then(res => {
        this.result2 = res
        if (this.result2 === 'failed') {
          this.$message({
            type: 'info',
            message: '项目库为空,请添加项目!'
          })
        } else {
          this.tableData = this.result2
        }
      })
  },
  methods: {
    subrepo () {
      this.$router.push({
        path: '/filerepo'
      })
    },
    corpus () {
      this.$router.push({
        path: '/repository'
      })
    },
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
    deletePending (scope) {
      DeletePending({
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

      this.pendData.splice(scope.$index, 1)
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
    handleChange1 (val) {
      this.currentRow1 = val
    },
    handleChange2 (val) {
      this.currentRow2 = val
    },
    setCurrent1 (row) {
      let extract = 'extract'
      let recommend = 'recommend'
      var ex = row[extract]
      var recom = row[recommend]
      console.log(ex)
      console.log(recom)
      this.$router.push({
        name: 'startsearch',
        params: {
          extractors: JSON.stringify(ex),
          recommends: JSON.stringify(recom)
        }
      })
    },
    setCurrent2 (row) {
      this.$refs.projectTable.setCurrentRow(row)
      var res = this.currentRow2
      let project = 'project'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === project && this.tableData[i][key] === res[project]) {
            var selectedProject = this.tableData[i][key]
            this.$router.push({
              path: '/projectinfo',
              query: {
                selectedProject: selectedProject
              }
            })
          }
        }
      }
    }
  }
}
</script>
