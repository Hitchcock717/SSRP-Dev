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
        <el-form-item label="搜索结果数(条)" prop="number">
          <el-input
            v-model="numberForm.number" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="view">查看项目信息</el-button>
          <el-button size="default" @click="submit" type="primary">确定</el-button>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
export default {
  data () {
    return {
      numberForm: {
        number: '13214',
        timeout: null
      }
    }
  },
  methods: {
    view () {
      this.$router.push('/complete')
    },
    submit () {
      this.$router.push('/simplesearch')
    }
  }
}
</script>
