<template>
  <d2-container>
    <d2-page-cover>
      <el-table :data="tableData" style="width: 900px" empty-text="N/A" max-height="550">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="摘要">
                <span>{{ props.row.abstract }}</span>
              </el-form-item>
              <el-form-item label="关键词">
                <span>{{ props.row.kws }}</span>
              </el-form-item>
              <el-form-item label="基金名称">
                <span>{{ props.row.fund }}</span>
              </el-form-item>
              <el-form-item label="引用量">
                <span>{{ props.row.cited }}</span>
              </el-form-item>
              <el-form-item label="下载量">
                <span>{{ props.row.downed }}</span>
              </el-form-item>
              <el-form-item label="相关链接">
                <span>{{ props.row.download }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" label="编号" align="center" width="50px">
        </el-table-column>
        <el-table-column prop="title" label="标题" align="center" width="200px">
        </el-table-column>
        <el-table-column prop="author" label="作者" align="center" width="200px">
        </el-table-column>
        <el-table-column prop="info" label="单位/机构" align="center" width="200px">
        </el-table-column>
        <el-table-column prop="date" label="发表时间" align="center" width="100px">
        </el-table-column>
        <el-table-column prop="source" label="来源" align="center" width="100px">
        </el-table-column>
      </el-table>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .d2-page-cover {
    @extend %full;
    @extend %unable-select;
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    align-items: center;
  }
</style>

<script>
import { GetRecommend } from '@/api/demo/recommend/getrecommendService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      tableData: []
    }
  },
  mounted () {
    GetRecommend({})
      .then(res => {
        this.result = res
        console.log(this.result)
        this.tableData = this.result
      })
  }
}
</script>
