<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="simpleForm" ref="simpleForm" label-width="150px" class="demo-simpleForm" :class='{fixed:isFixed}'>
        <el-form-item label="简单检索表达式" prop="expression">
          <el-button @click="viewQuery" type="primary" class="viewQuery">查看检索表达式</el-button>
        </el-form-item>
        <el-form-item label="过滤后结果数(条)" prop="number">
          <el-button @click="viewResult" type="primary" class="viewResult">查看搜索结果</el-button>
        </el-form-item>
        <el-form-item label="子库" prop="subrepo">
          <el-button @click="submit" type="primary" class="nextpage">进入子库</el-button>
        </el-form-item>
        <el-form-item label="导入结果" prop="import">
          <el-button
            @click="importResult"
            type="primary"
            class="importResult">导入</el-button>
        </el-form-item>
       </el-form>
       <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)" style="width: 800px" empty-text="N/A" max-height="500"
        highlight-current-row @current-change="handleChange" ref="simpleTable">
        <el-table-column label="编号" width="60px" prop="id"></el-table-column>
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
import { GetRawResult } from '@/api/demo/rawResult2Service'
export default {
  data () {
    return {
      storage: this.$route.params.storage, // 获取详情页面传递来的页面数据
      result: JSON.parse(this.$route.params.result),
      isFixed: '',
      currentPage: 1,
      currentRow: '',
      pagesize: 50,
      tableData: [],
      simpleForm: {
      }
    }
  },
  mounted () {
    if (localStorage.getItem('rawResult')) {
      console.log('1')
    } else { // key被清除, 无法获取
      this.tableData = this.storage
      console.log(this.tableData)
    }
  },
  methods: {
    importResult () {
      alert('正在导入...')
      GetRawResult({})
        .then(res => {
          this.rawResult = res
          alert('数据导入成功!')

          this.tableData = this.rawResult
          // console.log(this.tableData)
        })
        .catch(err => {
          console.log(err)
        })
    },
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
    viewQuery () {
      let queryBody = 'query'
      alert('您的简单检索表达式为: query = keyword in [' + this.result[queryBody] + ']')
    },
    viewResult () {
      let filterCount = 'filter_search_count'
      alert('过滤后搜索结果为' + this.result[filterCount] + '条!')
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

      // 点击详情，保存页面数据
      const parsed = JSON.stringify(this.tableData)
      localStorage.setItem('rawResult', parsed)

      let pkid = 'id'
      for (var i = 0, len = this.tableData.length; i < len; i++) {
        for (var key in this.tableData[i]) {
          if (key === pkid && this.tableData[i][key] === res[pkid]) {
            var selected = this.tableData[i]
            this.$router.push({
              path: '/detail1',
              query: {
                selected: JSON.stringify(selected)
              }
            })
            console.log(selected)
          }
        }
      }
    },
    handleChange (val) {
      this.currentRow = val
    },
    submit () { // 进入子库
      this.$router.push({
        name: 'subrepo',
        params: {
          rawResult: this.tableData
        }
      })
      console.log(this.rawResult)
    }
  },
  created () {
    window.addEventListener('scroll', this.onScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style scoped>
  .demo-simpleForm {
    margin-right: 100px;
    margin-top: 150px;
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
