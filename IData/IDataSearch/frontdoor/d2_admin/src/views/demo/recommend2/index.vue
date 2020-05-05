<template>
  <d2-container>
    <el-form :model="wordForm" ref="wordForm" label-width="250px" class="demo-wordForm" :class='{fixed:isFixed}'>
      <el-form-item>
        <el-button size="default" @click="handleSubmit" type="primary" class="button-complete">保存词汇</el-button>
      </el-form-item>
      <el-form-item>
        <el-table :data="extractData"
          style="width: 800px" empty-text="N/A" max-height="600">
          <el-table-column label="编号" width="100px" type="index" align="center"></el-table-column>
          <el-table-column label="抽取词汇" align="center" prop="originkws"></el-table-column>
          <el-table-column fixed="right" label="操作" width="100px" align="center">
            <template slot-scope="scope">
              <el-button size="small" type="text" @click="deleteExtractor(scope)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-form-item>
      <el-form-item>
        <el-table :data="recommendData"
          style="width: 800px" empty-text="N/A" max-height="600">
          <el-table-column label="编号" width="100px" type="index" align="center"></el-table-column>
          <el-table-column label="推荐词汇" align="center" prop="recommendkws"></el-table-column>
          <el-table-column fixed="right" label="操作" width="100px" align="center">
            <template slot-scope="scope">
              <el-button size="small" type="text" @click="deleteRecommend(scope)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-form-item>
    </el-form>
  </d2-container>
</template>

<script>
import { DeleteExtractor } from '@/api/demo/deletextractorService'
import { DeleteRecommend } from '@/api/demo/deleterecommendService'
export default {
  data () {
    return {
      isFixed: '',
      wordForm: {},
      extractData: [],
      recommendData: []
    }
  },
  mounted () {
    if (localStorage.getItem('results')) {
      this.results = JSON.parse(localStorage.getItem('results'))
      console.log(this.results)
      localStorage.removeItem('results')

      this.extractData = this.results[0]
      this.recommendData = this.results[1]
    }
  },
  methods: {
    deleteExtractor (scope) {
      DeleteExtractor({
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

      this.extractData.splice(scope.$index, 1)
    },
    deleteRecommend (scope) {
      DeleteRecommend({
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

      this.recommendData.splice(scope.$index, 1)
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
    handleSubmit () {
      this.$refs.wordForm.validate((valid) => {
        if (valid) {
          this.$router.push({
            path: '/complete',
            query: {
              extractors: JSON.stringify(this.extractData),
              recommends: JSON.stringify(this.recommendData)
            }
          })
          this.$message({
            type: 'success',
            message: '保存词汇成功!'
          })
        } else {
          this.$message({
            type: 'info',
            message: '保存词汇失败, 请重试!'
          })
        }
      })
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
 .demo-wordForm {
  margin-right: 250px;
  margin-top: 50px;
 }
 .button-save {
  float: right;
  margin-left: 25px;
 }
 .button-complete {
  float: right;
 }
 .demo-wordForm.fixed {
  position: fixed;
 }
 .select-item {
  width: 100px;
 }
 .input-with-select {
  width: 500px;
  background-color: #fff;
 }
 .extr {
  margin: 0 auto;
  max-width: 50%;
  text-align: center;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
 }
 .recom {
  margin: 0 auto;
  max-width: 50%;
  text-align: center;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
 }
 .box-card1 {
  width: 450px;
  margin-top: 50px;
 }
 .box-card2 {
  width: 450px;
 }
</style>
