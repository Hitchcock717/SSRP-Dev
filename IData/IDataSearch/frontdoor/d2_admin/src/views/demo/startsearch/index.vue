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
          <el-button type="primary" class="spider" @click="startSpider">启动爬虫</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { StartSpider } from '@/api/demo/spiderService'
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
  created () {
    this.$store.dispatch('d2admin/page/close', {
      tagName: '/complete'
    })
  },
  mounted () {
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
        spiders: ['idata'],
        extractors: this.$route.query.extractors,
        recommends: this.$route.query.recommends
      })
        .then(res => {
          this.result = res
          console.log(this.result)
          this.$message({
            type: 'success',
            message: '成功启动爬虫!'
          })
          this.$refs.searchForm.validate((valid) => {
            if (valid) {
              this.$router.push({
                path: '/notice1',
                query: {
                  result: JSON.stringify(this.result)
                }
              })
            }
          })
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
