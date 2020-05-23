<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :model="ruleForm" ref="ruleForm" label-width="250px" class="demo-ruleForm" :class='{fixed:isFixed}'>
        <el-form-item label="子库名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="子库说明" prop="desc">
          <el-input type="textarea" v-model="ruleForm.desc"></el-input>
        </el-form-item>
        <el-form-item label="子库存储位置" prop="region">
          <el-upload
            class="upload"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="fileList">
            <el-button size=”small“ type="primary">浏览</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="创建时间" required>{{gettime}}</el-form-item>
        <el-form-item label="领域词表" prop="subrepo">
          <el-button @click="subrepo" type="primary" class="nextpage">浏览</el-button>
        </el-form-item>
        <el-form-item label="选择发表时间" prop="date">
          <el-date-picker
            v-model="ruleForm.date"
            type="monthrange"
            align="right"
            unlink-panels
            range-separator="至"
            start-placeholder="开始月份"
            end-placeholder="结束月份"
            :picker-options="pickerOptions">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <el-button type="primary"
        @click="addRule"
        class="button-add">添加</el-button>
      <el-button type="primary"
        @click="complete"
        class="button-complete">完成</el-button>
      <span class="note">*为必填项；若有且仅有一条表达式，相邻关系选择'无'。</span>
      <el-table :data="tableData" style="width: 800px" max-height="500px">
        <el-table-column label="*搜索类型" prop="type">
          <template slot-scope="scope">
            <el-select v-model="tableData[scope.$index].type">
              <el-option label="标题" value="标题"></el-option>
              <el-option label="作者" value="作者"></el-option>
              <el-option label="机构/单位" value="机构/单位"></el-option>
              <el-option label="来源" value="来源"></el-option>
              <el-option label="基金" value="基金"></el-option>
              <el-option label="关键词" value="关键词"></el-option>
              <el-option label="摘要" value="摘要"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="*论文信息" prop="info">
          <template slot-scope="scope">
            <el-input type="textarea" autosize placeholder="输入关键词请用逗号分隔" v-model="tableData[scope.$index].info"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="搜索关系" prop="relation">
          <template slot-scope="scope">
            <el-select v-model="tableData[scope.$index].relation">
              <el-option label="并含" value="并含"></el-option>
              <el-option label="或含" value="或含"></el-option>
              <el-option label="不含" value="不含"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="论文信息" prop="otherinfo">
          <template slot-scope="scope">
            <el-input type="textarea" autosize placeholder="输入关键词请用逗号分隔" v-model="tableData[scope.$index].otherinfo"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="*启用正则" prop="regex">
          <template slot-scope="scope">
            <el-select v-model="tableData[scope.$index].regex">
              <el-option label="是" value="是"></el-option>
              <el-option label="否" value="否"></el-option>
            </el-select>
        </template>
        </el-table-column>
        <el-table-column label="*相邻表达式关系" prop="nextrelation">
          <template slot-scope="scope">
            <el-select v-model="tableData[scope.$index].nextrelation">
              <el-option label="无" value="无"></el-option>
              <el-option label="并且" value="并且"></el-option>
              <el-option label="或者" value="或者"></el-option>
              <el-option label="不含" value="不含"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="action" label="操作">
          <template slot-scope="scope">
            <el-button type="danger" @click="deleteRule(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-button type="primary" @click="submitForm" class="confirm">立即创建</el-button>
      <el-button type="primary" @click="resetForm('ruleForm')" class="reset">重置</el-button>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { GetExpression } from '@/api/demo/expressionService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      tableData: [],
      fileList: [],
      isFixed: '',
      gettime: this.getTime(),
      pickerOptions: {
        shortcuts: [{
          text: '本月',
          onClick (picker) {
            picker.$emit('pick', [new Date(), new Date()])
          }
        }, {
          text: '今年至今',
          onClick (picker) {
            const end = new Date()
            const start = new Date(new Date().getFullYear(), 0)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近六个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setMonth(start.getMonth() - 6)
            picker.$emit('pick', [start, end])
          }
        }]
      },
      ruleForm: {
        name: '',
        desc: ''
      }
    }
  },
  methods: {
    addRule () {
      this.tableData.push({})
    },
    deleteRule (index) {
      this.tableData.splice(index, 1)
    },
    complete () {
      let type = 'type'
      let info = 'info'
      let regex = 'regex'
      let nextrelation = 'nextrelation'

      var rawData = JSON.stringify(this.tableData)
      console.log(rawData)

      if (this.tableData.length === 0) {
        this.$message({
          type: 'info',
          message: '请添加检索表达式!'
        })
      }

      if (this.tableData.length !== 0) {
        for (var i = 0, len = this.tableData.length; i < len; i++) {
          let typeField = JSON.stringify(this.tableData[i][type])
          let infoField = JSON.stringify(this.tableData[i][info])
          let regexField = JSON.stringify(this.tableData[i][regex])
          let relationField = JSON.stringify(this.tableData[i][nextrelation])
          if (typeField === undefined || infoField === undefined || regexField === undefined || relationField === undefined) {
            this.$message({
              type: 'info',
              message: '必填项不能为空!'
            })
          } else {
            this.$message({
              type: 'success',
              message: '保存表达式成功!'
            })
          }
        }
      }
    },
    onScroll () {
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
      var offsetTop = this.$refs.wordForm.offsetTop
      console.log('scrollTop:' + scrollTop + 'offsetTop:' + offsetTop)
      if (scrollTop > offsetTop) {
        this.isFixed = true
      } else {
        this.isFixed = false
      }
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning('当前限制选择1个文件')
    },
    beforeRemove (file, fileList) {
      return this.$confirm('确定移除 $(file.name}?')
    },
    getTime: function () {
      // var _this = this
      let yy = new Date().getFullYear()
      let mm = new Date().getMonth() + 1
      let dd = new Date().getDate()
      let gettime = yy + '-' + mm + '-' + dd
      return gettime
    },
    subrepo () {
      this.$router.push('/repository')
    },
    submitForm () {
      var allData = JSON.parse(JSON.stringify(this.tableData))
      var pubDate = this.ruleForm.date

      if (JSON.stringify(allData) === '[{}]') {
        this.$message({
          type: 'info',
          message: '无法提交空表格!'
        })
      } else {
        if (pubDate === undefined) {
          var dateEmptyDict = { 'startdate': 'null', 'endate': 'null' }
          allData.push(dateEmptyDict)
          console.log(JSON.stringify(allData))
        } else {
          var startDate = JSON.stringify(pubDate[0]).substring(1, 11)
          var endDate = JSON.stringify(pubDate[1]).substring(1, 11)
          var dateDict = { 'startdate': startDate, 'endate': endDate }
          allData.push(dateDict)
          console.log(JSON.stringify(allData))
        }
        GetExpression({
          expression: JSON.stringify(allData),
          name: this.ruleForm.name,
          introduction: this.ruleForm.desc
        })
          .then(res => {
            this.result = res
            console.log(JSON.stringify(this.result))
            if (this.result !== 'failed') {
              this.$message({
                type: 'success',
                message: '创建成功!'
              })
              this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                  this.$router.push({
                    path: '/notice2',
                    query: {
                      result: JSON.stringify(this.result)
                    }
                  })
                }
              })
            } else {
              this.$message({
                type: 'info',
                message: '子库名称已经存在,请更改!'
              })
            }
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    resetForm (ruleForm) {
      this.$refs.ruleForm.resetFields()
    }
  },
  created () {
    window.addEventListener('scroll', this.onScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style scoped>
 .demo-ruleForm {
    margin-right: 200px;
    margin-top: 100px;
 }
 .el-input {
   width: 500px;
 }
 .input-with-select .el-input-group__prepend {
    width: 130px;
    background-color: #fff;
 }
 .select-item {
    width: 100px;
 }
 .el-table {
    margin-left: 100px;
 }
 .button-add {
    margin-left: 100px;
    margin-bottom: 10px;
 }
 .confirm {
    float: right;
    margin-top: 10px;
    margin-right: 50px;
 }
 .reset {
    float: right;
    margin-top: 10px;
    margin-right: 15px;
 }
 .note {
  margin-right: 30px;
  float: right;
 }
</style>
