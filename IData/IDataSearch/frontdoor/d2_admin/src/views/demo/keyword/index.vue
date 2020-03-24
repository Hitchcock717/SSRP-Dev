<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-form :inline="true" :model="wordForm" :rules="rules" ref="wordForm" label-width="190px" class="demo-wordForm">
        <el-form-item label="要查找的关键词" prop="word">
          <el-input type="text" class="el-select" v-model="wordForm.word" placeholder="请输入关键词" clearable filterable>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addItem">添加</el-button>
          <el-button size="default" @click="submit" type="primary" class="button-word">保存</el-button>
        </el-form-item>
        <div v-for="(item, index) in wordForm.dynamicItem" :key="index">
          <el-form-item
            label="AND"
            :prop="'dynamicItem.' + index + '.word'"
            :rules="rules">
            <el-input class="el-select" v-model="item.word" placeholder="请输入关键词" clearable
            filterable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="delete" @click="deleteItem(item, index)">删除</el-button>
          </el-form-item>
        </div>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import D2PageCover from './components/d2-page-cover'
export default {
  components: {
    D2PageCover
  },
  data () {
    return {
      wordForm: {
        word: '氨基酸',
        dynamicItem: []
      },
      rules: {
        word: [
          { required: true, message: '请输入关键词', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    addItem () {
      this.wordForm.dynamicItem.push({
        word: ''
      })
    },
    deleteItem (item, index) {
      this.wordForm.dynamicItem.splice(index, 1)
    },
    submit () {
      this.$refs.wordForm.validate((valid) => {
        if (valid) {
          this.$router.push('/complete')
        }
      })
    }
  }
}
</script>
