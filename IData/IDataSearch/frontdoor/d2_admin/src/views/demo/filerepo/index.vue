<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-table :data="tableData" ref="filerepoTable"
      style="width: 800px" empty-text="N/A" max-height="600" highlight-current-row @current-change="handleChange">
        <el-table-column label="编号" width="100px" type="index" align="center">
        </el-table-column>
        <el-table-column label="子库名称" align="center" prop="name">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button @click="setCurrent(scope.row)" type="text" size="small">详情</el-button>
            <el-button size="small" type="text" @click="deleteFilerepo(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .addFilerepo {
    margin-bottom: 15px;
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetFilerepo } from '@/api/demo/filerepo/getfilerepoService'
import { DeleteFilerepo } from '@/api/demo/filerepo/deletefilerepoService'
export default {
  data () {
    return {
      tableData: []
    }
  },
  created () {
    GetFilerepo({})
      .then(res => {
        this.result = res
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '论文库为空,请添加子库!'
          })
        } else {
          this.tableData = this.result
        }
      })
  },
  methods: {
    deleteFilerepo (scope) {
      DeleteFilerepo({
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
      this.$refs.filerepoTable.setCurrentRow(row)
      var res = this.currentRow
      console.log(res)
      let name = 'name'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === name && this.tableData[i][key] === res[name]) {
            var selectedFilerepo = this.tableData[i][key] // 数据库id作参数
            this.$router.push({
              path: '/file',
              query: {
                selectedFilerepo: JSON.stringify(selectedFilerepo)
              }
            })
            console.log(selectedFilerepo)
          }
        }
      }
    }
  }
}
</script>
