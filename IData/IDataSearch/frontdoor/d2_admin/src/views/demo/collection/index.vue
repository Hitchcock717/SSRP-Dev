<template>
  <d2-container class="page">
    <page-cover>
      <el-container style="height: 800px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-col :span="24">
            <el-menu
              default-active="2"
              class="el-menu-vertical-demo">
              <h4 class="d2-text-center">我的收藏夹</h4>
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
              <el-table-column label="编号" width="60px" prop="id" sortable></el-table-column>
              <el-table-column label="标题" width="100px" align="center" prop="title"></el-table-column>
              <el-table-column label="作者" prop="author"></el-table-column>
              <el-table-column label="发表时间" prop="date" sortable></el-table-column>
              <el-table-column label="被引频次" width="80px" prop="cited" sortable></el-table-column>
              <el-table-column label="下载频次" width="80px" prop="downed" sortable></el-table-column>
              <el-table-column fixed="right" label="操作" width="80">
                <template slot-scope="scope">
                  <el-button @click.native.prevent="viewRow(scope.$index, tableData)" type="text" size="small">
                  详情
                  </el-button>
                </template>
              </el-table-column>
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
  .abstract {
    margin-top: 20px;
  }
  .other {
    margin-top: 20px;
  }
  .note {
    margin-top: 20px;
  }
  .write {
    width: 190px;
    height: 50px;
  }
  .success {
    margin-top: 5px;
    float: right;
    margin-right: 5px;
  }
  .recom {
    margin-top: 50px;
  }
  .return {
    margin-top: 10px;
    float: right;
  }
</style>

<script>
export default {
  data () {
    return {
      currentPage: 1,
      pagesize: 5,
      tableData: [{
        id: '1',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2015-08-20',
        cited: '3',
        downed: '3221',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '2',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2018-09-20',
        cited: '3223',
        downed: '31',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '3',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '4',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '5',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '6',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '7',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '8',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '9',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
      }, {
        id: '10',
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        date: '2020-01-14',
        cited: '31',
        downed: '321',
        info: '北京大学物理学院电子显微镜实验室',
        source: '期刊',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        kws: '扫描电子显微镜； 信号探测器； 矿物'
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
