<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button
        @click="addFolder"
        type="primary"
        class="addFolder">添加</el-button>
      <el-button
        @click="importResult"
        type="primary"
        class="importResult">导入</el-button>
      <el-table :data="tableData" ref="repoTable"
      style="width: 800px" empty-text="N/A" max-height="600" highlight-current-row @current-change="handleChange">
        <el-table-column label="编号" width="100px" type="index" align="center">
        </el-table-column>
        <el-table-column label="收藏夹名称" align="center" prop="folder">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button @click="setCurrent(scope.row)" type="text" size="small">详情</el-button>
            <el-button size="small" type="text" @click="deleteFolder(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .addFolder {
    margin-bottom: 15px;
  }
</style>

<script>
// import { mapState, mapActions } from 'vuex'
import { GetFolder } from '@/api/demo/folder/getfolderService'
import { AddFolder } from '@/api/demo/folder/addfolderService'
import { DeleteFolder } from '@/api/demo/folder/deletefolderService'
export default {
  data () {
    return {
      tableData: []
    }
  },
  methods: {
    importResult () {
      GetFolder({})
        .then(res => {
          this.result = res
          if (this.result === 'failed') {
            alert('该词表为空,请添加词汇!')
          } else {
            this.tableData = this.result
          }
        })
    },
    addFolder () {
      this.$prompt('请输入收藏夹名称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /[\u4e00-\u9fa5_a-zA-Z0-9_]{4,10}/,
        inputErrorMessage: '收藏夹名称长度必须为4-10位'
      }).then(({ value }) => {
        AddFolder({
          foldername: value
        })
          .then(res => {
            this.feedback = res
            console.log(this.feedback)
            if (this.feedback !== 'failed') {
              this.$message({
                type: 'success',
                message: '新建收藏夹名称是: ' + value
              })
              this.tableData.push(this.feedback)
            } else {
              this.$message({
                type: 'info',
                message: '收藏夹已存在!'
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
    deleteFolder (scope) {
      DeleteFolder({
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
      let folder = 'folder'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === folder && this.tableData[i][key] === res[folder]) {
            var selectedCollection = this.tableData[i][key] // 数据库id作参数
            this.$router.push({
              path: '/collection',
              query: {
                selectedCollection: JSON.stringify(selectedCollection)
              }
            })
            console.log(selectedCollection)
          }
        }
      }
    }
  }
}
</script>
