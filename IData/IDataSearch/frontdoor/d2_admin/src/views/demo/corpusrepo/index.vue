<template>
  <d2-container class="page">
    <page-cover>
      <el-container style="height: 800px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-col :span="24">
            <el-menu
              default-active="2"
              class="el-menu-vertical-demo">
              <h4 class="d2-text-center">我的词表库</h4>
              <el-submenu index="1">
                <template slot="title">
                  <i class="el-icon-location"></i>
                  <span>电镜相关</span>
                </template>
                <el-menu-item-group>
                  <template slot="title">分组一</template>
                  <el-menu-item index="1-1">选项1</el-menu-item>
                  <el-menu-item index="1-2">选项2</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group title="分组2">
                  <el-menu-item index="1-3">选项3</el-menu-item>
                </el-menu-item-group>
                <el-submenu index="1-4">
                  <template slot="title">选项4</template>
                  <el-menu-item index="1-4-1">选项1</el-menu-item>
                </el-submenu>
              </el-submenu>
              <el-menu-item index="2">
                <i class="el-icon-menu"></i>
                <span slot="title">氨基酸相关</span>
              </el-menu-item>
              <el-menu-item index="3">
                <i class="el-icon-document"></i>
                <span slot="title">中药相关</span>
              </el-menu-item>
              <el-menu-item index="4">
                <i class="el-icon-setting"></i>
                <span slot="title">机器人相关</span>
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-aside>
        <el-container>
          <el-main>
            <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            style="width: 800px" empty-text="N/A" max-height="600">
              <el-table-column label="编号" width="80px" prop="id" sortable></el-table-column>
              <el-table-column label="词汇" align="center" prop="phrase"></el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[5, 10, 15]"
              :page-size="1"
              layout="total, sizes, prev, pager, next, jumper"
              :total="tableData.length">
            </el-pagination>
          </el-main>
        </el-container>
      </el-container>
    </page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .page-cover {
    @extend %full;
    @extend %unable-select;
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    align-items: center;
  }
  .el-header {
    color: #333;
    line-height: 60px;
  }
  .el-aside {
    color: #333;
  }
</style>

<script>
export default {
  data () {
    return {
      currentPage: 1,
      pagesize: 10,
      tableData: [{
        id: '1',
        phrase: '扫描电子显微镜'
      }, {
        id: '2',
        phrase: '信号探测器'
      }, {
        id: '3',
        phrase: '矿物'
      }, {
        id: '4',
        phrase: '透射电子显微镜'
      }, {
        id: '5',
        phrase: '纳米地球科学'
      }, {
        id: '6',
        phrase: '纳米矿物'
      }, {
        id: '7',
        phrase: '超微结构'
      }, {
        id: '8',
        phrase: '微区原位分析'
      }, {
        id: '9',
        phrase: '图像锐度'
      }, {
        id: '10',
        phrase: '扫描电子显微镜'
      }, {
        id: '11',
        phrase: 'X射线能谱仪'
      }, {
        id: '12',
        phrase: '表面'
      }, {
        id: '13',
        phrase: '非弹性平均自由程'
      }, {
        id: '14',
        phrase: '薄膜'
      }, {
        id: '15',
        phrase: '采集电路'
      }, {
        id: '16',
        phrase: '非弹性散射'
      }, {
        id: '17',
        phrase: '表征原子'
      }, {
        id: '18',
        phrase: '多层膜'
      }, {
        id: '19',
        phrase: 'SEM-EDS'
      }, {
        id: '20',
        phrase: '加速电压'
      }]
    }
  },
  methods: {
    handleSizeChange (val) {
      this.pagesize = val
    },
    handleCurrentChange (val) {
      this.currentPage = val
    },
    viewRow (index, rows) {
      this.$router.push('/detail1')
    },
    submit () {
      this.$router.push('/simplesearch')
    }
  }
}
</script>
