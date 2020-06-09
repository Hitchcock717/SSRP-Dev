<template>
  <d2-container class="page">
    <d2-page-cover>
      <div class="block">
        <el-carousel height="200px'" type="card" :interval="4000">
          <el-carousel-item v-for="item in imgList" :key="item.id">
            <el-row>
              <el-col :span="24" class="banner_img">
                <img ref="bannerHeight" :src="item.url" class="bannerImg" @load="imgLoad"/>
              </el-col>
            </el-row>
          </el-carousel-item>
        </el-carousel>
      </div>
      <el-form :model="searchForm" ref="searchForm" label-width="100px" class="demo-Form">
        <el-form-item>
          <el-button type="primary" class="spider" @click="startSpider">开始检索</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { StartSpider } from '@/api/demo/spiderService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      spiders: ['idata'],
      height: '',
      imgList: [{
        id: 0,
        url: require('./img/spider.png')
      },
      {
        id: 1,
        url: require('./img/spider.png')
      },
      {
        id: 2,
        url: require('./img/spider.png')
      }],
      searchForm: {
      }
    }
  },
  mounted () {
    console.log(this.$route.params.extractors)
    console.log(this.$route.params.recommends)
    this.imgLoad()
    window.addEventListener('resize', () => {
      this.bannerHeight = this.$refs.bannerHeight[0].height
      this.imgLoad()
    }, false)
  },
  methods: {
    imgLoad () {
      this.$nextTick(() => {
        this.bannerHeight = this.$refs.bannerHeight[0].height
        console.log(this.$refs.bannerHeight[0].height)
      })
    },
    startSpider () {
      this.$message({
        type: 'success',
        message: '正在启动...'
      })
      StartSpider({
        extractors: this.$route.params.extractors,
        recommends: this.$route.params.recommends
      })
        .then(res => {
          this.result = res
          console.log(this.result)
          if (this.result !== 'failed') {
            this.$message({
              type: 'success',
              message: '您的搜索字段成功命中, 立即获取相应数据!'
            })
            this.$refs.searchForm.validate((valid) => {
              if (valid) {
                this.$router.push({
                  name: 'notice3',
                  params: {
                    result: JSON.stringify(this.result),
                    time: this.$route.params.time
                  }
                })
              }
            })
          } else {
            this.$message({
              type: 'info',
              message: '很遗憾, 暂无现成数据, 请等候邮件通知!'
            })
            this.$refs.searchForm.validate((valid) => {
              if (valid) {
                this.$router.push({
                  name: 'notice1',
                  params: {
                    extractors: this.$route.params.extractors,
                    recommends: this.$route.params.recommends
                  }
                })
              }
            })
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style scoped>
  .block {
    width: 800px;
  }
  .el-form {
    width: 310px;
  }
  .spider {
    margin-top: 20px;
    margin-left: 250px;
  }
  .save {
    margin-top: 20px;
    margin-left: 250px;
  }
  .el-carousel__item:nth-child(2n) {
     background-color: #99a9bf;
  }
  .el-carousel__item:nth-child(2n+1) {
     background-color: #d3dce6;
  }
</style>
