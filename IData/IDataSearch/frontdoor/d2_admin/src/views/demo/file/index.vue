<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button type="primary" class="return" @click="submit">返回论文库</el-button>
        <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            style="width: 800px" empty-text="N/A" max-height="550">
          <el-table-column label="数据库编号" width="80px" align="center" prop="pk"></el-table-column>
          <el-table-column label="标题" width="300px" align="center" prop="title"></el-table-column>
          <el-table-column label="作者" width="150px" align="center" prop="author"></el-table-column>
          <el-table-column label="单位/机构" width="100px" align="center" prop="info"></el-table-column>
          <el-table-column label="发表时间" width="100px" prop="date" sortable></el-table-column>
          <el-table-column fixed="right" label="操作" width="70px" align="center">
            <template slot-scope="scope">
              <el-button @click="viewRow(scope)" type="text" size="small">
              详情
              </el-button>
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
  }
</style>

<script>
// import { mapState } from 'vuex'
import { GetFile } from '@/api/demo/file/getfileService'
export default {
  data () {
    return {
      selectedFilerepo: this.$route.query.selectedFilerepo,
      currentPage: 1,
      pagesize: 10,
      options: [],
      tableData: []
    }
  },
  created () {
    GetFile({
      name: this.selectedFilerepo
    })
      .then(res => {
        this.result = res
        console.log(this.result)
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '请求失败,请重试!'
          })
        } else {
          this.tableData = this.result
        }
      })
  },
  methods: {
    viewRow (scope) {
      let id = 'pk'
      console.log(scope.row[id])
      this.$router.push({
        path: '/detail2',
        query: {
          selected: scope.row[id]
        }
      })
    },
    handleSizeChange (val) {
      this.pagesize = val
    },
    handleCurrentChange (val) {
      this.currentPage = val
    },
    submit () {
      this.$router.push({
        path: '/filerepo'
      })
    }
  }
}
</script>
