<template>
  <d2-container class="page">
    <d2-page-cover>
      <el-upload
        action="https://jsonplaceholder.typicode.com/posts/"
        ref="upload"
        drag
        multiple
        accept=".txt"
        :file-list="fileList"
        :limit="3"
        :on-exceed="handleExceed"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传txt文件，且不超过10mb</div>
      </el-upload>
      <el-button size="default" @click="submit(fileList)" type="primary" class="button-save">保存</el-button>
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
      fileList: [{
        name: 'test1.txt',
        url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
      },
      {
        name: 'test2.txt',
        url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
      }]
    }
  },
  methods: {
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning('当前限制选择 3 个文件，本次选择文件数量过多！')
    },
    beforeRemove (file, fileList) {
      return this.$confirm('确定移除此文件？')
    },
    submit (fileList) {
      if (this.fileList.length > 0) {
        this.$router.push('/complete')
      }
    }
  }
}
</script>

<style scoped>
  .button-save {
    float: right;
  }
</style>
