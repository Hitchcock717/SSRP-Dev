<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button
        @click="addRepository"
        type="primary"
        class="addRepository">添加</el-button>
      <el-table :data="tableData" ref="repoTable"
      style="width: 800px" empty-text="N/A" max-height="600" highlight-current-row @current-change="handleChange">
        <el-table-column label="编号" width="100px" type="index" align="center">
        </el-table-column>
        <el-table-column label="词表名称" align="center" prop="repository">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button @click="setCurrent(scope.row)" type="text" size="small">详情</el-button>
            <el-button size="small" type="text" @click="deleteRepository(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .addRepository {
    margin-bottom: 15px;
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetRepository } from '@/api/demo/repository/getrepositoryService'
import { AddRepository } from '@/api/demo/repository/addrepositoryService'
import { DeleteRepository } from '@/api/demo/repository/deleterepositoryService'
export default {
  data () {
    return {
      tableData: []
    }
  },
  created () {
    GetRepository({})
      .then(res => {
        this.result = res
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '该词表库为空,请添加分组!'
          })
        } else {
          this.tableData = this.result
        }
      })
  },
  methods: {
    addRepository () {
      this.$prompt('请输入词表名称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /[\u4e00-\u9fa5_a-zA-Z0-9_]{4,10}/,
        inputErrorMessage: '词表名称长度必须为4-10位'
      }).then(({ value }) => {
        AddRepository({
          reponame: value
        })
          .then(res => {
            this.feedback = res
            if (this.feedback !== 'failed') {
              this.$message({
                type: 'success',
                message: '新建词表名称是: ' + value
              })
              this.tableData.push(this.feedback)
            } else {
              this.$message({
                type: 'info',
                message: '词表已存在!'
              })
            }
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        })
      })
    },
    deleteRepository (scope) {
      DeleteRepository({
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
      this.$refs.repoTable.setCurrentRow(row)
      var res = this.currentRow
      console.log(res)
      let repo = 'repository'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === repo && this.tableData[i][key] === res[repo]) {
            var selectedCorpus = this.tableData[i][key] // 数据库id作参数
            this.$router.push({
              path: '/corpus',
              query: {
                selectedCorpus: JSON.stringify(selectedCorpus)
              }
            })
            console.log(selectedCorpus)
          }
        }
      }
    }
  }
}
</script>
