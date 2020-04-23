<template>
  <d2-container>
    <d2-page-cover>
      <el-container style="height: 800px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu :default-openeds="['1', '3']" class="corpus">
            <el-submenu index="1">
              <template slot="title"><i class="el-icon-message"></i><router-link to="/page1">词表库</router-link></template>
              <el-menu-item-group>
                <template slot="title">分组一</template>
                <el-menu-item index="1-1">电镜词表</el-menu-item>
                <el-menu-item index="1-2">氨基酸词表</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
          <div class="note">
            <el-button round size="mini" class="selectedItem" v-for="(item,index) in selectedItems" :key="index">{{item.name}} <i class="red fa fa-close (alias)"
            v-on:click="deleteSelectedItem($index)"></i></el-button>
            <input v-model="inputItem" placeholder="请输入想要收藏的词汇" class="write" type="text" v-on:focus="showDropmenu" v-on:keyup.enter="addItem">
            <el-button type="primary" class="success" @click="addItem">确定</el-button>
          </div>
          <div v-show="isShowDropmenu">
            <p class="recom">推荐词</p>
            <div v-for="item in cataList" v-show="item.isShow" :key="item">
                <el-button round type="mini" v-for="(one,index) in item.items" class="item" v-on:click="addByClick(one)" :key="index">{{one}}</el-button>
            </div>
          </div>
        </el-aside>
        <el-container>
          <el-main>
            <el-table :data="tableData" class="basicinfo">
              <el-table-column prop="title" label="标题" width="250">
              </el-table-column>
              <el-table-column prop="author" label="作者" width="100">
              </el-table-column>
              <el-table-column prop="info" label="单位/机构">
              </el-table-column>
              <el-table-column prop="date" label="发表时间" width="80">
              </el-table-column>
              <el-table-column prop="source" label="来源" width="80">
              </el-table-column>
            </el-table>
            <el-table :data="detailData" class="abstract">
              <el-table-column prop="abstract" label="摘要" width="610">
              </el-table-column>
              <el-table-column fixed="right" label="操作" align="center" width="80">
                <template slot-scope="scope">
                  <el-button @click.native.prevent="viewRow(scope.$index, tableData)" type="text" size="small">收藏</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-table :data="otherData" class="other">
              <el-table-column prop="kws" label="关键词">
              </el-table-column>
              <el-table-column prop="fund" label="基金">
              </el-table-column>
              <el-table-column prop="cited" label="被引频次" width="80">
              </el-table-column>
              <el-table-column prop="downed" label="下载频次" width="80">
              </el-table-column>
            </el-table>
            <el-button type="primary" class="import" @click="importResult">导入详情结果</el-button>
            <el-button type="primary" class="return" @click="submit">返回检索结果页</el-button>
          </el-main>
        </el-container>
      </el-container>
    </d2-page-cover>
  </d2-container>
</template>
<style lang="scss" scoped>
  .d2-page-cover {
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
  .corpus {
    margin-top: 80px;
  }
  .basicinfo {
    margin-top: 60px;
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
  .import {
    margin-top: 10px;
    margin-left: 20px;
    float: right;
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
      selected: this.$route.params.selected, // params传参页面刷新即消失
      tableData: [],
      detailData: [],
      otherData: [],
      selectedItems: [{
        name: '生物电镜'
      }],
      isShowDropmenu: true,
      inputItem: '',
      cataList: [{
        isShow: true,
        items: [ '光学显微镜', '透射显微镜', '冷冻电镜' ]
      }, {
        isShow: true,
        items: [ '天冬氨酸', '亮氨酸', '烟酰胺' ]
      }]
    }
  },
  methods: {
    importResult () {
      console.log(this.selected)
      // data in table 1
      let title = 'title'
      let author = 'author'
      let source = 'source'
      let info = 'info'
      let date = 'date'
      var tableDict1 = { 'title': this.selected[title], 'author': this.selected[author], 'source': this.selected[source], 'info': this.selected[info], 'date': this.selected[date] }
      this.tableData = Array(1).fill(tableDict1)

      // data in table 2
      let abstract = 'abstract'
      var tableDict2 = { 'abstract': this.selected[abstract] }
      this.detailData = Array(1).fill(tableDict2)

      // data in table 3
      let kws = 'kws'
      let fund = 'fund'
      let cited = 'cited'
      let downed = 'downed'
      var tableDict3 = { 'kws': this.selected[kws], 'fund': this.selected[fund], 'cited': this.selected[cited], 'downed': this.selected[downed] }
      this.otherData = Array(1).fill(tableDict3)
    },
    showDropmenu: function (event) {
      console.log('showDropmenu')
      this.isShowDropmenu = true
    },
    addItem () {
      if (this.inputItem !== '') {
        this.selectedItems.push({ name: this.inputItem })
        this.inputItem = ''
        console.log(this.selected)
      }
    },
    deleteSelectedItem (index) {
      this.selectedItems.splice(index, 1)
    },
    showCataList (index) {
      var i = this.cataList.length

      while (i--) {
        i === index ? this.cataList[i].isShow = true : this.cataList[i].isShow = false
      }
    },
    addByClick (name) {
      var i = this.selectedItems.length
      while (i--) {
        if (this.selectedItems[i].name === name) {
          return
        }
      }
      this.selectedItems.push({ name: name })
    },
    submit () {
      this.$router.push('/detailsearch')
    }
  }
}
</script>
