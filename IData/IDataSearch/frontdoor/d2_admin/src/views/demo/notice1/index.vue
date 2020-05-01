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
          <el-button size="default" @click="dialog = true" type="primary" class="view">查看检索统计</el-button>
          <el-button size="default" @click="submit" type="primary" class="confirm">确定</el-button>

          <el-drawer
            title="您的搜索结果"
            :visible.sync="dialog"
            direction="rtl"
            custom-class="demo-drawer"
            ref="drawer"
            >
            <div class="demo-drawer__content">
              <el-form :model="viewForm">
                <el-form-item label="搜索词" prop="keyword" :label-width="formLabelWidth">
                  <el-button @click="viewKeyword" type="primary" class="viewKeyword">查看</el-button>
                </el-form-item>
                <el-form-item label="简单检索表达式" prop="expression" :label-width="formLabelWidth">
                  <el-button @click="viewQuery" type="primary" class="viewQuery">查看</el-button>
                </el-form-item>
                <el-form-item label="未过滤结果数(条)" prop="rawnumber" :label-width="formLabelWidth">
                  <el-button @click="viewRawResult" type="primary" class="viewRawResult">查看</el-button>
                </el-form-item>
                <el-form-item label="过滤后结果数(条)" prop="number" :label-width="formLabelWidth">
                  <el-button @click="viewResult" type="primary" class="viewResult">查看</el-button>
                </el-form-item>
              </el-form>
              <div class="demo-drawer__footer">
                <el-button @click="cancelForm" type="primary" class="in_confirm">确 定</el-button>
              </div>
            </div>
          </el-drawer>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      result: JSON.parse(this.$route.query.result),
      formLabelWidth: '150px',
      numberForm: {},
      timer: null,
      viewForm: {
        keyword: '',
        expression: '',
        rawnumber: '',
        number: ''
      }
    }
  },
  methods: {
    viewKeyword () {
      let keyword = 'keywords'
      alert('您的搜索词为:' + this.result[keyword])
    },
    viewQuery () {
      let queryBody = 'query'
      alert('您的简单检索表达式为: query = keyword in [' + this.result[queryBody] + ']')
    },
    viewRawResult () {
      let rawCount = 'raw_search_count'
      alert('未过滤搜索结果为' + this.result[rawCount] + '条!')
    },
    viewResult () {
      let filterCount = 'filter_search_count'
      alert('过滤后搜索结果为' + this.result[filterCount] + '条!')
    },
    cancelForm () {
      this.loading = false
      this.dialog = false
      clearTimeout(this.timer)
    },
    submit () {
      this.$router.push({
        path: '/simplesearch'
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
  .in_confirm {
    float: right;
    margin-top: 25px;
    margin-right: 15px;
  }
  .view {
    margin-left: 500px;
  }
</style>
