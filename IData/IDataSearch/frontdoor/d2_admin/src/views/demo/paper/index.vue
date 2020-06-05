<template>
  <d2-container>
    <d2-page-cover>
      <el-steps :active="2" class="process" space="20%" align-center="true">
        <el-step title="选择检索方式" description="请选择输入论文信息检索或上传词表搜索"></el-step>
        <el-step title="准备检索" description="请按提示输入检索信息或上传格式正确的词表"></el-step>
        <el-step title="完成项目创建" description="项目信息保存完毕"></el-step>
        <el-step title="创建子库" description="获取更有价值的数据并分析"></el-step>
        <el-step title="完成子库创建" description="子库信息保存完毕"></el-step>
      </el-steps>
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
          <el-input placeholder="输入关键词(中文逗号分隔)" v-model="textForm.body" class="input-with-select">
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
          this.$router.push({
            path: '/recommend',
            query: {
              name: this.$route.query.name
            }
          })
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
