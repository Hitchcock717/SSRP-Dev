<template>
  <d2-container>
    <el-form :model="wordForm" ref="wordForm" label-width="250px" class="demo-wordForm" :class='{fixed:isFixed}'>
      <el-form-item>
        <el-button size="default" @click="handleSubmit" type="primary" class="button-complete">保存词汇</el-button>
      </el-form-item>
      <el-form-item>
        <el-card class="box-card1">
          <h3 class="d2-text-center">抽取关键词</h3>
          <p v-if="extractors.length === 0" class="d2-text-center">无抽取词汇</p>
          <ul class="extr" v-for="(extr, index) in extractors" :key="index">
            <li class="extr-index">id: {{index}}</li>
            <li class="extr-originkws">抽取词: {{extr.originkws}}</li>
            <el-button type="danger" size="primary" icon="el-icon-delete" @click="deleteExtractor(extr.pk)" class="button-delete">删除</el-button>
          </ul>
        </el-card>
      </el-form-item>
      <el-form-item>
        <el-card class="box-card2">
          <h3 class="d2-text-center">推荐关键词</h3>
          <p v-if="recommends.length === 0" class="d2-text-center">无推荐词汇</p>
          <ul class="recom" v-for="(recom, index) in recommends" :key="index">
            <li class="recom-index">id: {{index}}</li>
            <li class="recom-recommendkws">推荐词: {{recom.recommendkws}}</li>
            <el-button type="danger" size="priamry" icon="el-icon-delete" @click="deleteRecommend(recom.pk)" class="button-delete">删除</el-button>
          </ul>
        </el-card>
      </el-form-item>
    </el-form>
  </d2-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  data () {
    return {
      isFixed: '',
      wordForm: {
      }
    }
  },
  computed: {
    ...mapState('expand/extractors', {
      extractors: state => state.extractors
    }),
    ...mapState('expand/recommends', {
      recommends: state => state.recommends
    }),
    ...mapState('d2admin/page', [
      'current'
    ])
  },
  methods: {
    ...mapActions('expand/extractors', [
      'deleteExtractor'
    ]),
    ...mapActions('expand/recommends', [
      'deleteRecommend'
    ]),
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
              extractors: JSON.stringify(this.extractors),
              recommends: JSON.stringify(this.recommends)
            }
          })
          console.log(JSON.stringify(this.extractors))
          this.$message({
            type: 'success',
            message: '成功保存词汇!'
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
    this.$store.dispatch('expand/extractors/getExtractors')
    this.$store.dispatch('expand/recommends/getRecommends')
    this.$store.dispatch('d2admin/page/close', {
      tagName: this.current
    })
  },
  destroyed () {
    window.removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style scoped>
 .demo-wordForm {
  margin-right: 100px;
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
