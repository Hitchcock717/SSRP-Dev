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
      <el-form :model="searchForm" :rules="rules" ref="searchForm" label-width="100px" class="demo-Form">
        <el-form-item label="搜索方式" prop="method">
          <el-select id="search" v-model="searchForm.method" placeholder="请选择搜索方式">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
              name="method">{{item.label}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click=submit(searchForm)>确定</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
export default {
  data () {
    return {
      imgList: [{
        id: 0,
        url: require('./img/demo.jpg')
      },
      {
        id: 1,
        url: require('./img/demo.jpg')
      }],
      options: [{
        value: '选项1',
        label: '论文搜索'
      }, {
        value: '选项2',
        label: '词表搜索'
      }],
      searchForm: {
        method: ''
      },
      rules: {
        method: [
          { required: true, message: '请选择搜索方式', trigger: 'change' }
        ]
      },
      mounted () {
        this.imgLoad()
        window.addEventListener('resize', () => {
          this.bannerHeight = this.$refs.bannerHeight[0].height
          this.imgLoad()
        }, false)
      }
    }
  },
  methods: {
    imgLoad () {
      this.$nextTick(() => {
        this.bannerHeight = this.$refs.bannerHeight[0].height
        console.log(this.$refs.bannerHeight[0].height)
      })
    },
    submit (searchForm) {
      this.$refs.searchForm.validate((valid) => {
        if (valid) {
          if (this.searchForm.method === '选项1') {
            this.$router.push({
              path: '/paper',
              query: {
                method: 'papersearch'
              }
            })
          } else if (this.searchForm.method === '选项2') {
            this.$router.push({
              path: '/corpusearch',
              query: {
                method: 'corpusearch'
              }
            })
          }
        }
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
    float: right;
    width: 310px;
  }
  .el-form-item {
    float: right;
  }
  .el-button {
    float: right;
    width: 80px;
  }
  .el-carousel__item:nth-child(2n) {
     background-color: #99a9bf;
  }
  .el-carousel__item:nth-child(2n+1) {
     background-color: #d3dce6;
  }
</style>
