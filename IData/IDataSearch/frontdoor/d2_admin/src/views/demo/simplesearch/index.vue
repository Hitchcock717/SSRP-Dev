<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="simpleForm" :simples="simples" ref="simpleForm" label-width="150px" class="demo-simpleForm">
        <el-form-item label="简单检索表达式" prop="expression">
          <span>{{ query }}</span>
        </el-form-item>
        <el-form-item label="搜索结果数(条)" prop="number">
          <el-button @click="viewResult(result)" type="primary" class="viewResult">查看搜索结果</el-button>
          <span class="number">{{ result }}</span>
        </el-form-item>
        <el-form-item label="子库" prop="subrepo">
          <el-button @click="submit" type="primary" class="nextpage">进入子库</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)" stripe=true style="width: 800px" fit="true" empty-text="N/A" :default-sort = "{prop: 'id', order: 'descending'}" max-height="300">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="编号:">
                <span>{{props.row.id}}</span>
              </el-form-item>
              <el-form-item label="标题:">
                <span>{{props.row.title}}</span>
              </el-form-item>
              <el-form-item label="作者:">
                <span>{{props.row.author}}</span>
              </el-form-item>
              <el-form-item label="单位/机构:">
                <span>{{props.row.info}}</span>
              </el-form-item>
              <el-form-item label="来源:">
                <span>{{props.row.source}}</span>
              </el-form-item>
              <el-form-item label="关键词:">
                <span>{{props.row.kws}}</span>
              </el-form-item>
              <el-form-item label="发表时间:">
                <span>{{props.row.date}}</span>
              </el-form-item>
              <el-form-item label="被引频次:">
                <span>{{props.row.cited}}</span>
              </el-form-item>
              <el-form-item label="下载频次:">
                <span>{{props.row.downed}}</span>
              </el-form-item>
              <el-form-item label="基金:">
                <span>{{props.row.fund}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="编号" width="60px" prop="id" sortable></el-table-column>
        <el-table-column label="标题" width="250px" align="center" prop="title"></el-table-column>
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
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data () {
    return {
      simples: '',
      query: 'query = keywords in ' + this.$route.query.keywords,
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
      }],
      simpleForm: {
      }
    }
  },
  computed: {
    ...mapState('expand/results', {
      result: state => state.result
    })
  },
  methods: {
    viewResult (result) {
      this.result.push(result)
    },
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
      this.$router.push('/subrepo')
    }
  },
  created () {
    this.$store.dispatch('expand/results/getResult')
  }
}
</script>

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }
  .el-table-column {
    align: center;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 60%;
  }
  .el-pagination {
    float: right;
  }
</style>
