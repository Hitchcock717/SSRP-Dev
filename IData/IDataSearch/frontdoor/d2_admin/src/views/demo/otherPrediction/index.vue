<template>
  <d2-container>
    <d2-page-cover>
      <el-button type="primary"
        @click="otherReturn"
        class="button-return">返 回</el-button>
      <el-form :model="textForm" ref="textForm" label-width="250px" class="demo-textForm">
        <el-form-item label='请选择预测领域' prop="type">
          <el-select v-model="textForm.subject" class='select-item' placeholder="请选择">
            <el-option label="学者推荐" value="recommend"></el-option>
            <el-option label="学者研究兴趣预测" value="predict"></el-option>
          </el-select>
        </el-form-item>
        <div v-if="textForm.subject=='recommend'">
          <el-form-item label="推荐领域">
            <el-input v-model="textForm.region" placeholder="请填入领域名称" class="col-sm-8"></el-input>
          </el-form-item>
          <el-form-item label="推荐学者数量">
            <el-input type="text" v-model="textForm.number" placeholder="请填入数字" class="col-sm-8"></el-input>
          </el-form-item>
        </div>
        <div v-if="textForm.subject=='predict'">
          <el-form-item label="学者库编号查询">
            <span class="explain">https://www.aminer.cn/scikg</span>
          </el-form-item>
          <el-form-item label="Aminer学者编号">
            <el-input v-model="textForm.pid" placeholder="请填入编号" class="col-sm-8"></el-input>
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary"
            @click="otherPrediction()"
            class="button-add">开始预测</el-button>
        </el-form-item>
        <el-form-item>
          <hr/>
        </el-form-item>
      </el-form>
      <el-tabs class="tabs">
        <el-tab-pane label="学者推荐" name="recommend">
          <el-table :data="scholarData">
            <el-table-column prop="id" label="Aminer学者库编号" align="center">
            </el-table-column>
            <el-table-column prop="url" label="Aminer学者库链接" align="center">
            </el-table-column>
            <el-table-column prop="L2 distance" label="L2距离" align="center">
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="学者研究兴趣预测" name="predict">
          <el-table :data="paperData">
            <el-table-column prop="group" label="类别" align="center">
            </el-table-column>
            <el-table-column prop="name" label="研究方向" align="center">
            </el-table-column>
            <el-table-column prop="p" label="预测得分" align="center">
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </d2-page-cover>
  </d2-container>
</template>

<script>
// 测试学者编号: 53f432b7dabfaeb2ac02dc61
import { ScholarRecommend } from '@/api/demo/prediction/scholarRecommendService'
import { PaperPrediction } from '@/api/demo/prediction/paperPredictionService'
// import { mapState } from 'vuex'
export default {
  data () {
    return {
      scholarData: [],
      paperData: [],
      textForm: {
        subject: '',
        region: '',
        number: '',
        papernumber: ''
      },
      rules: {
        subject: [
          { type: 'array', required: true, message: '请至少选择一个领域', trigger: 'change' }
        ],
        region: [
          { required: true, message: '请填写推荐领域', trigger: 'blur' }
        ],
        number: [
          { required: true, message: '请填写推荐学者数量', trigger: 'blur' }
        ],
        pid: [
          { required: true, message: '请填写学者编号', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    otherReturn () {
      this.$router.push({
        path: '/analysis'
      })
    },
    otherPrediction () {
      if (this.textForm.subject === 'recommend') {
        ScholarRecommend({
          text: this.textForm.region,
          num: this.textForm.number
        })
          .then(res => {
            var result = res
            console.log(result)
            if (result !== 'failed') {
              this.scholarData = result
              this.$message({
                type: 'success',
                message: '解析成功, 请点击下方tab!'
              })
            } else {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            }
          })
      } else {
        PaperPrediction({
          pid: this.textForm.pid
        })
          .then(res => {
            var result = res
            if (result === 'failed') {
              this.$message({
                type: 'info',
                message: '解析失败, 请重试!'
              })
            } else if (result === 'No result') {
              this.$message({
                type: 'info',
                message: '该学者无发表刊物!'
              })
            } else {
              this.paperData = result
              this.$message({
                type: 'success',
                message: '解析成功, 请点击下方tab!'
              })
            }
          })
      }
    }
  }
}
</script>

<style scoped>
 .demo-textForm {
  margin-right: 200px;
  margin-top: 100px;
 }
 .select-item {
  width: 300px;
 }
 .input-with-select {
  width: 500px;
  background-color: #fff;
 }
 .button-return {
  margin-bottom: 30px;
  margin-right: 200px;
  float: right;
 }
</style>
