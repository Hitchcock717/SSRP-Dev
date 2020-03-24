/* eslint-disable */
<template>
  <d2-container>
    <d2-page-cover>
      <el-container style="height: 800px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu :default-openeds="['1', '3']">
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
            <el-button round size="mini" class="selectedItem" v-for="item in selectedItems" :key="item">{{item.name}} <i class="red fa fa-close (alias)"
            v-on:click="deleteSelectedItem($index)"></i></el-button>
            <input v-model="inputItem" placeholder="请输入想要收藏的词汇" class="write" type="text" v-on:focus="showDropmenu" v-on:keyup.enter="addItem">
            <el-button type="primary" class="success" @click="addItem">确定</el-button>
          </div>
          <div v-show="isShowDropmenu">
            <p class="recom">推荐词</p>
            <div v-for="item in cataList" v-show="item.isShow" :key="item">
                <el-button round type="mini" v-for="one in item.items" class="item" v-on:click="addByClick(one)" :key="item">{{one}}</el-button>
            </div>
          </div>
        </el-aside>
        <el-container>
          <el-main>
            <el-table :data="tableData">
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
    const item = {
        title: '扫描电子显微镜显微分析技术在地球科学中的应用',
        author: '陈莉; 徐军; 陈晶',
        info: '北京大学物理学院电子显微镜实验室',
        date: '2015-08-20',
        source: '期刊'
      },
      item2 = {
        abstract: '阐述了扫描电子显微镜的基本原理、图像种类、各种信号的主要特性,并对扫描电子显微镜显微分析技术在地球科学研究领域的应用现状、前景进行了评述.场发射扫描电子显微镜分辨率高,可以实现极微区的原位精细观察和研究.具备低真空模式的扫描电子显微镜,对于不具有导电性的地质样品,无需蒸镀导电膜,即可直接实现矿物等样品表面的观察分析,显示具有广泛的应用前景.装配背散射探头、X射线能谱仪、阴极荧光谱仪、背散射电子衍射仪等附件的扫描电子显微镜,可同时获取地质样品的多重信息,如:微区尺度形貌像、阴极荧光分析、背散射图像、成分信息、晶体结构特征等.本文通过实例讨论了扫描电子显微镜的地质应用,并强调阴极荧光谱仪在地学研究中的应用不应局限于矿物结构图像分析,尚应加强阴极荧光谱峰的矿物成因分析应用,其可有效揭示矿物晶格缺陷、微量元素组成差异,有助于更精准地进行矿物生长条件重建.'
      },
      item3 = {
        kws: '扫描电子显微镜； 信号探测器； 矿物',
        fund: '国家自然科学基金项目(批准号:41402031)资助',
        cited: '3',
        downed: '3221'
      }
    return {
      tableData: Array(1).fill(item),
      detailData: Array(1).fill(item2),
      otherData: Array(1).fill(item3),
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
    showDropmenu: function (event) {
      console.log('showDropmenu')
      this.isShowDropmenu = true
    },
    // hideDropmenu: function (event) {
    // this.isShowDropmenu = false
    // console.log('hideDropmenu')
    // },
    test: function () {
      console.log('test')
    },
    addItem: function () {
      if (this.inputItem !== '') {
        this.selectedItems.push({ name: this.inputItem })
        this.inputItem = ''
      }
    },
    deleteSelectedItem: function (index) {
      this.selectedItems.splice(index, 1)
    },
    showCataList: function (index) {
      var i = this.cataList.length

      while (i--) {
        i === index ? this.cataList[i].isShow = true : this.cataList[i].isShow = false
      }
    },
    addByClick: function (name) {
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
