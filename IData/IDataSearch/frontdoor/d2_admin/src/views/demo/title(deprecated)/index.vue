<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :inline="true" :model="textForm" :rules="rules" ref="textForm" label-width="250px" class="demo-textForm">
        <el-form-item class="d2-mr-80" label="要查找的标题" prop="text">
          <el-input type="textarea" class="el-select" v-model="textForm.text" placeholder="请输入论文标题" maxlength="50" show-word-limit clearable filterable>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addItem" class="button-text">添加</el-button>
          <el-button size="default" @click="submit" type="primary" class="button-save">保存</el-button>
        </el-form-item>
        <el-form-item class="d2-mr-80" label="提取出的关键词" prop="keyword">
          <el-checkbox :indeterminate="isIndeterminate" v-model="textForm.checkAll" @change="handleCheckAllChange">全选</el-checkbox>
          <el-checkbox-group class="group" v-model="textForm.keyword" size="medium" fill="#409EFF">
            <el-checkbox
              v-for="item in checkList"
              :key="item"
              :label="item"
              :value="item"
              name="keyword"
              @change="handleCheckKeysChange"
              border>
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <div v-for="(item, index) in textForm.dynamicItem" :key="index">
          <el-form-item
            class="d2-mr-80"
            label="AND"
            :prop="'dynamicItem.' + index + '.text'"
            :rules="rules">
            <el-input class="el-select" type="textarea" v-model="item.text" maxlength="50" show-word-limit placeholder="请输入论文标题" clearable
            filterable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="delete" @click="deleteItem(item, index)">删除</el-button>
          </el-form-item>
          <el-form-item class="d2-mr-80" label="提取出的关键词" prop="keyword">
            <el-checkbox :indeterminate="isIndeterminate" v-model="textForm.checkOther" @change="handleCheckOtherAllChange">全选</el-checkbox>
            <el-checkbox-group class="group" v-model="textForm.keyword" size="medium" fill="#409EFF">
              <el-checkbox
                v-for="item in otherList"
                :key="item"
                :label="item"
                :value="item"
                name="keyword"
                @change="handleCheckOtherKeysChange"
                border>
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import D2PageCover from './components/d2-page-cover'
const keys = ['脑膜瘤', '免疫组化', '电镜']
export default {
  components: {
    D2PageCover
  },
  data () {
    return {
      checkList: keys,
      otherList: [],
      textForm: {
        checkAll: false,
        isIndeterminate: true,
        text: ' 脑膜瘤临床病理、免疫组化和电镜观察',
        dynamicItem: [],
        keyword: []
      },
      rules: {
        text: [
          { required: true, message: '请输入论文标题', trigger: 'blur' }
        ],
        keyword: [
          { type: 'array', required: true, message: '请至少选择一个关键词', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    handleCheckAllChange (val) {
      this.textForm.keyword = val ? keys : []
      this.isIndeterminate = false
    },
    handleCheckedCitiesChange (value) {
      let checkedCount = value.length
      this.checkAll = checkedCount === this.keys.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.keys.length
    },
    addItem () {
      this.textForm.dynamicItem.push({
        text: ''
      })
    },
    deleteItem (item, index) {
      this.textForm.dynamicItem.splice(index, 1)
    },
    submit () {
      this.$refs.textForm.validate((valid) => {
        if (valid) {
          this.$router.push('/complete')
        }
      })
    }
  }
}
</script>

<style scoped>
 .demo-textForm {
  margin-right: 200px;
 }
 .el-select {
   float: left;
   width: 105%;
   margin-left: 5px;
   margin-right: 100px;
 }
 .button-text {
  margin-left: 35px;
 }
 .delete {
  margin-left: 35px;
 }
</style>
