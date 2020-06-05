<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-steps :active="3" class="process" space="20%" align-center="true">
        <el-step title="选择检索方式" description="请选择输入论文信息检索或上传词表搜索"></el-step>
        <el-step title="准备检索" description="请按提示输入检索信息或上传格式正确的词表"></el-step>
        <el-step title="完成项目创建" description="项目信息保存完毕"></el-step>
        <el-step title="创建子库" description="获取更有价值的数据并分析"></el-step>
        <el-step title="完成子库创建" description="子库信息保存完毕"></el-step>
      </el-steps>
      <div class="block">
        <el-timeline>
          <el-timeline-item type="success" placement="top">
            <el-card>
              <i slot="prepend" class="el-icon-success"></i>
              <h4>项目创建成功</h4>
            </el-card>
          </el-timeline-item>
          <el-timeline-item placement="top">
            <el-card>
              <h4>正在为您搜索...</h4>
              <h4>搜索完成后, 将会向您发送提示邮件</h4>
              <h4>收到邮件后, 您可以进入项目仓库——待办项目获取您的搜索结果</h4>
              <p nowrap>搜索开始时间为: {{ gettime }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
      <el-button size="default" @click="submit" type="primary" class="confirm">退 出</el-button>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { Scrapy } from '@/api/demo/scrapyService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      gettime: this.getTime()
    }
  },
  created () {
    Scrapy({
      extractors: this.$route.params.extractors,
      recommends: this.$route.params.recommends
    })
      .then(res => {
        console.log(res)
      })
  },
  methods: {
    getTime: function () {
      let yy = new Date().getFullYear()
      let mm = new Date().getMonth() + 1
      let dd = new Date().getDate()
      let hh = new Date().getHours()
      let min = new Date().getMinutes()
      let sec = new Date().getSeconds()
      if (sec < 10) {
        sec = '0' + sec
      }
      let gettime = yy + '-' + mm + '-' + dd + ' ' + hh + ':' + min + ':' + sec
      return gettime
    },
    submit () {
      this.$router.push({
        path: '/index'
      })
    }
  }
}
</script>

<style scoped>
  .block {
    width: 600px;
  }
  .confirm {
    float: right;
    margin-top: 20px;
    margin-right: 30px;
  }
</style>
