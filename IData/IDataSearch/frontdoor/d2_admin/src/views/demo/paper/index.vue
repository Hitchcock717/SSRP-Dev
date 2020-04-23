<template>
  <d2-container>
    <d2-page-cover>
      <el-form :model="textForm" ref="textForm" label-width="250px" class="demo-textForm">
        <el-form-item>
          <el-button size="default" @click="handleSubmit" type="primary" class="button-save">查看推荐词汇</el-button>
        </el-form-item>
        <el-form-item label='请选择搜索类型' prop="type">
          <el-select v-model="textForm.subject" class='select-item' placeholder="请选择">
            <el-option label="关键词" value="关键词"></el-option>
            <el-option label="标题" value="标题"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label='请输入论文信息' prop="text">
          <el-input placeholder="输入关键词请用逗号分隔" v-model="textForm.body" class="input-with-select">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary"
            @click="addMessage({ subject: textForm.subject, body: textForm.body})"
            :disabled="!textForm.subject || !textForm.body"
            class="button-add">添加</el-button>
        </el-form-item>
        <el-form-item>
          <hr/>
        </el-form-item>
        <el-form-item>
          <el-card class="box-card">
            <h3 class="d2-text-center">要搜索的论文信息</h3>
            <p v-if="messages.length === 0" class="d2-text-center">无信息</p>
            <div class="msg" v-for="(msg, index) in messages" :key="index">
              <p class="msg-index">id: {{index}}</p>
              <p class="msg-subject">搜索类型: {{msg.subject}}</p>
              <p class="msg-body">搜索内容: {{msg.body}}</p>
              <el-button type="danger" size="small" icon="el-icon-delete" circle @click="deleteMessage(msg.pk)" class="button-delete">删除</el-button>
            </div>
          </el-card>
        </el-form-item>
      </el-form>
    </d2-page-cover>
  </d2-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'Messages',
  data () {
    return {
      textForm: {
        subject: '',
        body: ''
      }
    }
  },
  computed: {
    ...mapState('expand/messages', {
      messages: state => state.messages
    })
  },
  methods: {
    ...mapActions('expand/messages', [
      'addMessage',
      'deleteMessage'
    ]),
    handleSubmit () {
      this.$refs.textForm.validate((valid) => {
        if (valid) {
          this.$router.push('/recommend')
        }
      })
    }
  }
}
</script>

<style scoped>
 .demo-textForm {
  margin-right: 200px;
  margin-top: 200px;
 }
 .button-save {
  float:right;
 }
 .button-add {
  float:right;
  margin-top: 20px;
  margin-left: 35px;
 }
 .button-delete {
  margin-left: 25px;
 }
 .select-item {
  width: 100px;
 }
 .input-with-select {
  width: 500px;
  background-color: #fff;
 }
 .msg {
  margin: 0 auto;
  max-width: 80%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 10px;
 }
 .msg-index {
  /* margin-bottom: 0; */
 }
 .box-card {
  width: 500px;
 }
</style>
