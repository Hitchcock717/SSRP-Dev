<template>
  <d2-container class="page">
    <d2-page-cover>
       <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)" style="width: 800px" empty-text="N/A" max-height="500"
        highlight-current-row @current-change="handleChange" ref="simpleTable">
        <el-table-column label="编号" width="60px" type="index"></el-table-column>
        <el-table-column label="标题" width="250px" align="center" prop="title"></el-table-column>
        <el-table-column label="作者" prop="author"></el-table-column>
        <el-table-column label="发表时间" prop="date" sortable></el-table-column>
        <el-table-column label="被引频次" width="80px" prop="cited" sortable></el-table-column>
        <el-table-column label="下载频次" width="80px" prop="downed" sortable></el-table-column>
        <el-table-column fixed="right" label="操作" width="80">
          <template slot-scope="scope">
            <el-button @click="setCurrent(scope.row)" type="text" size="small">
            详情
            </el-button>
          </template>
        </el-table-column>
       </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[50, 100]"
        :page-size="50"
        layout="total, sizes, prev, pager, next, jumper"
        :total="tableData.length">
      </el-pagination>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { GetFilterResult, GetPreRecord } from '@/api/demo/filterResultService'
import { mapState } from 'vuex'
export default {
  data () {
    return {
      height: '',
      currentPage: 1,
      currentRow: '',
      pagesize: 50,
      tableData: []
    }
  },
  computed: {
    ...mapState('d2admin/page', [
      'current'
    ])
  },
  methods: {
    handleSizeChange (val) {
      this.pagesize = val
    },
    handleCurrentChange (val) {
      this.currentPage = val
    },
    setCurrent (row) {
      this.$refs.simpleTable.setCurrentRow(row)
      var res = this.currentRow

      let pkid = 'id'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === pkid && this.tableData[i][key] === res[pkid]) {
            var selected = this.tableData[i][key]
            this.$router.push({
              path: '/detail2',
              query: {
                selected: JSON.stringify(selected)
              }
            })
          }
        }
      }
    },
    handleChange (val) {
      this.currentRow = val
    },
    submit () {
      this.$router.push({
        path: '/analysis'
      })
    }
  },
  beforeRouteEnter (to, from, next) {
    if (from.name === 'detail2') {
      next(vm => {
        let id = localStorage.getItem('record_id')
        GetPreRecord({ record_id: id })
          .then(res => {
            localStorage.removeItem('record_id')
            console.log('from detail')
            console.log(res)
            vm.filterResult = res.result
            vm.tableData = vm.filterResult
            localStorage.setItem('record_id', res.record_id)
          }).catch(err => {
            console.log(err)
          })
      })
    } else {
      next(vm => {
        GetFilterResult({})
          .then(res => {
            console.log('others')
            console.log(res)
            vm.filterResult = res.result
            vm.tableData = vm.filterResult
            localStorage.setItem('record_id', res.record_id)
          })
          .catch(err => {
            console.log(err)
          })
      })
    }
  },
  created () {
    this.$store.dispatch('d2admin/page/close', {
      tagName: this.current
    })

    window.addEventListener('scroll', this.onScroll)

    this.$message({
      type: 'success',
      message: '正在启动...'
    })
  },
  destroyed () {
    window.removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }
  .el-table-column {
    align: center;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 60%;
  }
  .el-pagination {
    float: right;
  }
</style>
