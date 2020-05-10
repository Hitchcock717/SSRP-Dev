<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-button type="primary" class="return" @click="submit">返回收藏夹</el-button>
        <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            style="width: 800px" empty-text="N/A" max-height="550">
          <el-table-column label="编号" width="60px" align="center" type="index"></el-table-column>
          <el-table-column label="标题" width="300px" align="center" prop="title"></el-table-column>
          <el-table-column label="作者" width="150px" align="center" prop="author"></el-table-column>
          <el-table-column label="单位/机构" width="100px" align="center" prop="info"></el-table-column>
          <el-table-column label="发表时间" width="100px" prop="date" sortable></el-table-column>
          <el-table-column fixed="right" label="操作" width="90px" align="center">
            <template slot-scope="scope">
              <el-button @click="viewRow(scope)" type="text" size="small">
              详情
              </el-button>
              <el-button size="small" type="text" @click="deleteCollection(scope)">删除</el-button>
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
// import { mapState, mapActions } from 'vuex'
import { GetCollection } from '@/api/demo/collection/getcollectionService'
import { DeleteCollection } from '@/api/demo/collection/deletecollectionService'
export default {
  data () {
    return {
      selectedCollection: this.$route.query.selectedCollection,
      currentPage: 1,
      pagesize: 10,
      options: [],
      tableData: []
    }
  },
  created () {
    this.$store.dispatch('d2admin/page/close', {
      tagName: '/folder'
    })

    GetCollection({
      collection: this.selectedCollection
    })
      .then(res => {
        this.result = res
        console.log(this.result)
        if (this.result === 'failed') {
          this.$message({
            type: 'info',
            message: '该分组为空,请添加论文!'
          })
        } else {
          this.tableData = this.result
        }
      })
  },
  mounted () {
    // 获取收藏夹, 清除key
    if (localStorage.getItem('folders')) {
      this.folders = JSON.parse(localStorage.getItem('folders'))
      console.log(this.folders)
      localStorage.removeItem('folders')
    } else {
      console.log('No folders')
    }
  },
  methods: {
    deleteCollection (scope) {
      DeleteCollection({
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
    viewRow (scope) {
      let flag = 'flag'
      this.$router.push({
        path: '/detail1',
        query: {
          selected: scope.row[flag]
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
        name: 'folder',
        params: {
          storage: this.folders // 传输页面数据
        }
      })
    }
  }
}
</script>
