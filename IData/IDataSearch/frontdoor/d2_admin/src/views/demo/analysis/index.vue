<template>
  <d2-container class="page">
    <d2-page-cover>
    <div class="img-warp">
      <div class="block" @click="dialogFormVisible = true">
        <span class="demonstration">智能预测平台</span>
        <div class="basic-image">
          <img ref="bannerHeight" :src="basicurl" class="basicImg" @load="imgLoad"/>
        </div>
      </div>
      <div class="block" @click="AdvanceSearch()">
        <span class="demonstration">文献分析平台</span>
        <div class="advance-image">
          <img ref="bannerHeight" :src="advanceurl" class="advanceImg" @load="imgLoad"/>
        </div>
      </div>
    </div>
    <el-dialog title="选择预测版块" :visible.sync="dialogFormVisible">
      <el-form :model="analysisForm">
        <el-form-item label="标题分类预测" :label-width="formLabelWidth">
          <el-button type="primary" @click="titlePrediction()">进 入</el-button>
        </el-form-item>
        <el-form-item label="作者特征预测" :label-width="formLabelWidth">
          <el-button type="primary" @click="authorPrediction()">进 入</el-button>
        </el-form-item>
        <el-form-item label="学者推荐&著作预测" :label-width="formLabelWidth">
          <el-button type="primary" @click="otherPrediction()">进 入</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { GetFilerepo } from '@/api/demo/filerepo/getfilerepoService'
export default {
  data () {
    return {
      bannerHeight: '200px',
      basicurl: require('./img/basic.png'),
      advanceurl: require('./img/advance.png'),
      analysisForm: {},
      formLabelWidth: '250px',
      dialogFormVisible: false
    }
  },
  mounted () {
    this.imgLoad()
    window.addEventListener('resize', () => {
      this.bannerHeight = this.$refs.bannerHeight[0].height
      this.imgLoad()
    }, false)

    GetFilerepo({})
      .then(res => {
        this.result = res
      })
  },
  methods: {
    imgLoad () {
      this.$nextTick(() => {
        this.bannerHeight = this.$refs.bannerHeight[0].height
        console.log(this.$refs.bannerHeight[0].height)
      })
    },
    titlePrediction () {
      this.$router.push({
        path: '/titlePrediction'
      })
    },
    authorPrediction () {
      this.$router.push({
        path: '/authorPrediction'
      })
    },
    otherPrediction () {
      this.$router.push({
        path: '/otherPrediction'
      })
    },
    AdvanceSearch () {
      this.$router.push({
        name: 'Advanceanalysis',
        params: {
          file: JSON.stringify(this.result)
        }
      })
    }
  }
}
</script>

<style scoped>
  .img-warp {
    width: 500px;
    margin: 0 -8px;
    &:after{
      display:block;
      clear:both;
      visibility: hidden;
      height:0;
      content:"";
    }
  }
  .block {
    float:left;
    width: 50%;
    padding: 10px 8px;
    box-sizing: border-box;
    img{
      width: 100%;
    }
  }
</style>
