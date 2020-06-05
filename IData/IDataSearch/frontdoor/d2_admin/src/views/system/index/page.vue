<template>
  <d2-container class="page">
    <d2-page-cover>
      <d2-icon-svg class="logo" name="d2-admin"/>
      <template slot="footer">
        <div class="btn-group">
          <span class="btn-group__btn" @click="$open('https://github.com/d2-projects')">开源组织</span> |
          <span class="btn-group__btn" @click="$open('https://d2.pub/zh/doc/d2-admin')">文档</span> |
          <span class="btn-group__btn" @click="$open('https://github.com/d2-projects/d2-admin-start-kit')">简化版</span> |
          <span class="btn-group__btn" @click="$open('https://juejin.im/user/57a48b632e958a006691b946/posts')">掘金</span> |
          <el-popover :width="172" trigger="hover">
            <p class="d2-mt-0 d2-mb-10">今日前端</p>
            <img src="./image/qr@2x.png" style="width: 172px;">
            <span slot="reference" class="btn-group__btn btn-group__btn--link">
              <d2-icon name="weixin"/>
              微信公众号
            </span>
            <p style="font-size: 12px; margin-top: 0px; margin-bottom: 0px;">
              官方公众号，主要推送前端技术类文章、框架资源、学习教程，以及 D2 系列项目更新信息
            </p>
          </el-popover>
        </div>
        <el-tooltip class="item1" effect="dark" content="首次进入请完善个人信息" placement="top">
          <el-button type="primary" size="large" class="enter1" @click="personal">填 写 个 人 信 息</el-button>
        </el-tooltip>
        <el-tooltip class="item2" effect="dark" content="如有疑问请先阅读平台说明文档" placement="top">
          <el-button type="primary" size="large" class="enter2" @click="submit">创 建 项 目</el-button>
        </el-tooltip>
        <d2-help/>
      </template>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import D2Help from './components/d2-help'
import D2PageCover from './components/d2-page-cover'
export default {
  components: {
    D2Help,
    D2PageCover
  },
  data () {
    return {
      filename: __filename
    }
  },
  methods: {
    submit () {
      this.$router.push({
        path: '/project'
      })
    },
    personal () {
      this.$router.push({
        path: '/personal'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  .logo {
    width: 120px;
  }
  .enter2 {
    margin-top: 15px;
    margin-bottom: 15px;
  }
  .btn-group {
    color: $color-text-placehoder;
    font-size: 12px;
    line-height: 12px;
    margin-top: 0px;
    margin-bottom: 20px;
    .btn-group__btn {
      color: $color-text-sub;
      &:hover {
        color: $color-text-main;
      }
      &.btn-group__btn--link {
        color: $color-primary;
      }
    }
  }
}
</style>
