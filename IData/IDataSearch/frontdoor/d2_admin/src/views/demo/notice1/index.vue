<template>
  <d2-container class="page">
    <d2-page-cover>
      <div class="block">
        <el-timeline>
          <el-timeline-item type="success" timestamp="2020/3/22" placement="top">
            <el-card>
              <i slot="prepend" class="el-icon-success"></i>
              <h4>项目demo创建成功</h4>
              <p>admin 创建于 2020/3/22 20:46</p>
            </el-card>
          </el-timeline-item>
          <el-timeline-item timestamp="2020/3/22" placement="top">
            <el-card>
              <h4>正在为您搜索...</h4>
              <h4>搜索完成后，将会向您发送提示邮件</h4>
              <p>admin 提交于 2020/3/22 20:46</p>
            </el-card>
          </el-timeline-item>
          <el-timeline-item type="success" timestamp="2020/3/23" placement="top">
            <el-card>
              <h4>搜索完成，邮件已发送</h4>
              <h4>请在”已有项目“中查看搜索结果</h4>
              <p>admin 提交于 2020/3/23 20:46</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
      <el-form :inline="true" :model="numberForm" ref="numberForm" label-width="190px" class="demo-numberForm">
        <el-form-item>
          <el-button size="default" @click="view" type="primary" class="view">查看搜索结果</el-button>
          <el-button size="default" @click="submit" type="primary" class="confirm">确定</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
export default {
  data () {
    return {
      result: JSON.parse(this.$route.query.result),
      numberForm: {
      }
    }
  },
  methods: {
    view () {
      let count = 'raw_search_count'
      alert('已为您初步搜索到' + this.result[count] + '条数据!')
    },
    submit () {
      this.$router.push({
        path: '/simplesearch',
        query: {
          result: JSON.stringify(this.result)
        }
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
    margin-right: 25px;
  }
  .view {
    margin-left: 500px;
  }
</style>
