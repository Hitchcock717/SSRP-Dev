<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="simpleForm" ref="simpleForm" label-width="150px" class="demo-simpleForm" :class='{fixed:isFixed}'>
        <el-form-item label="子库入口" prop="subrepo">
          <el-button @click="submit" type="primary" class="nextpage">创建子库</el-button>
        </el-form-item>
      </el-form>
      <div v-if="tableData">
         <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)" style="width: 800px" empty-text="N/A" max-height="550"
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
      </div>
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
import { GetRawResult, GetPreRecord } from '@/api/demo/rawResultService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      height: '',
      isFixed: '',
      currentPage: 1,
      currentRow: '',
      pagesize: 50,
      tableData: [],
      simpleForm: {}
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
            var selected = this.tableData[i][key] // 数据库id作参数
            this.$router.push({
              path: '/detail1',
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
    submit () { // 进入子库
      this.$router.push('/subrepo')
    }
  },
  beforeRouteEnter (to, from, next) {
    if (from.name === 'detail1') {
      next(vm => {
        let id = localStorage.getItem('record_id')
        GetPreRecord({ record_id: id })
          .then(res => {
            localStorage.removeItem('record_id')
            console.log('from detail')
            console.log(res)
            vm.rawResult = res.result
            vm.tableData = vm.rawResult
            localStorage.setItem('record_id', res.record_id)
          })
          .catch(err => {
            console.log(err)
          })
      })
    } else {
      next(vm => {
        GetRawResult({})
          .then(res => {
            console.log('others')
            console.log(res)
            vm.rawResult = res.result
            vm.tableData = vm.rawResult
            localStorage.setItem('record_id', res.record_id)
          })
          .catch(err => {
            console.log(err)
          })
      })
    }
  },
  created () {
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
  .demo-simpleForm {
    margin-right: 100px;
  }
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
