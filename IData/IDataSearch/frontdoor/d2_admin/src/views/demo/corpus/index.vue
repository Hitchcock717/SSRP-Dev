<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button type="primary" class="return" @click="submit">返回词表库</el-button>
      <el-button
        @click="addCorpus"
        type="primary"
        class="addCorpus">添加</el-button>
      <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      style="width: 800px" empty-text="N/A" max-height="600">
        <el-table-column label="编号" width="100px" type="index" align="center"></el-table-column>
        <el-table-column label="词汇" align="center" prop="kws"></el-table-column>
        <el-table-column fixed="right" label="操作" width="100px" align="center">
          <template slot-scope="scope">
            <el-button size="small" type="text" @click="deleteCorpus(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 15]"
        :page-size="1"
        layout="total, sizes, prev, pager, next, jumper"
        :total="tableData.length">
      </el-pagination>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .return {
    margin-bottom: 15px;
    margin-right: 10px;
  }
  .addCorpus {
    margin-bottom: 15px;
    float: right;
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetCorpus } from '@/api/demo/corpus/getcorpusService'
import { AddCorpus } from '@/api/demo/corpus/addcorpusService'
import { DeleteCorpus } from '@/api/demo/corpus/deletecorpusService'
export default {
  data () {
    return {
      selectedCorpus: this.$route.query.selectedCorpus,
      currentPage: 1,
      pagesize: 10,
      options: [],
      tableData: []
    }
  },
  created () {
    GetCorpus({
      corpus: this.selectedCorpus
    })
      .then(res => {
        this.result = res
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '该词表为空,请添加词汇!'
          })
        } else {
          this.tableData = this.result
        }
      })
  },
  methods: {
    addCorpus () {
      this.$prompt('请输入词汇名称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /[\u4e00-\u9fa5_a-zA-Z0-9_]{1,30}/,
        inputErrorMessage: '词汇名称长度必须为1-30位'
      }).then(({ value }) => {
        AddCorpus({
          kws: value,
          corpus: this.selectedCorpus
        })
          .then(res => {
            this.feedback = res
            console.log(this.feedback)
            if (this.feedback !== 'failed') {
              this.$message({
                type: 'success',
                message: '添加词汇名称是: ' + value
              })
              this.tableData.push(this.feedback)
            } else {
              this.$message({
                type: 'info',
                message: '词汇已存在!'
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
    deleteCorpus (scope) {
      DeleteCorpus({
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
    handleSizeChange (val) {
      this.pagesize = val
    },
    handleCurrentChange (val) {
      this.currentPage = val
    },
    submit () {
      this.$router.push({
        path: '/repository'
      })
    }
  }
}
</script>
