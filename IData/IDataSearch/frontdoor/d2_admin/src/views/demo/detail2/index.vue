<template>
  <d2-container>
    <d2-page-cover>
      <el-container style="height: 800px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu :default-openeds="['1', '3']" class="corpus">
            <el-submenu index="1">
              <template slot="title"><i class="el-icon-message"></i><router-link to="/page1">收藏词汇</router-link></template>
            </el-submenu>
          </el-menu>
          <div class="note">
            <el-button round size="mini" class="selectedItem" v-for="(item,index) in selectedItems" :key="index">{{item.name}}<i class="red fa fa-close (alias)"
            v-on:click="deleteSelectedItem($index)"></i></el-button>
            <input v-model="inputItem" placeholder="Enter确认" class="write" type="text" v-on:focus="showDropmenu" v-on:keyup.enter="addItem">
            <el-button type="primary" class="success" @click="corpusFormVisible = true">收藏词汇</el-button>
          </div>
          <div v-show="isShowDropmenu">
            <p class="recom">推荐词</p>
            <div v-for="item in cataList" v-show="item.isShow" :key="item">
                <el-button round type="mini" v-for="one in item.items" class="item" v-on:click="addByClick(one)" :key="one">{{one}}</el-button>
            </div>
          </div>
        </el-aside>
        <el-dialog title="词表库地址" :visible.sync="corpusFormVisible">
          <el-form :model="corpusform">
            <el-form-item label="您的词表库" :label-width="formLabelWidth">
              <el-select v-model="corpusform.repository">
                <el-option class="repo" v-for="(repo, index) in repositorys" :key="index" :label="repo.repository" :value="repo.repository"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="corpusFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="addCorpus(corpusFormVisible)">确 定</el-button>
          </div>
        </el-dialog>
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
              <el-table-column fixed="right" label="操作" align="center" width="80">
                <template>
                  <el-button @click="dialogFormVisible = true" type="text" size="small">收藏</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-table :data="detailData" class="abstract">
              <el-table-column prop="abstract" label="摘要" width="610">
              </el-table-column>
              <el-table-column prop="source" label="来源" width="80">
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
          <el-dialog title="收藏夹地址" :visible.sync="dialogFormVisible">
            <el-form :model="collectform">
              <el-form-item label="您的收藏夹" :label-width="formLabelWidth">
                <el-select v-model="collectform.folder">
                  <el-option class="fold" v-for="(fold, index) in folders" :key="index" :label="fold.folder" :value="fold.folder"></el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="addCollection(dialogFormVisible)">确 定</el-button>
            </div>
        </el-dialog>
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
  .return {
    margin-top: 10px;
    float: right;
  }
</style>

<script>
import { GetSelectedFilterResult } from '@/api/demo/selectedFilterResultService'
import { AddCollection } from '@/api/demo/collection/addcollectionService'
import { AppendCorpus } from '@/api/demo/corpus/appendcorpusService'
import { GetFolder } from '@/api/demo/folder/getfolderService'
import { GetRepository } from '@/api/demo/repository/getrepositoryService'
export default {
  data () {
    return {
      selected: this.$route.query.selected, // params传参页面刷新即消失
      folders: this.folders,
      repositorys: this.repositorys,
      tableData: [],
      detailData: [],
      otherData: [],
      selectedItems: [],
      isShowDropmenu: true,
      inputItem: '',
      cataList: [{
        isShow: true,
        items: [ '光学显微镜', '透射显微镜', '冷冻电镜' ]
      }, {
        isShow: true,
        items: [ '天冬氨酸', '亮氨酸', '烟酰胺' ]
      }],
      collectform: {
        folder: ''
      },
      corpusform: {
        repository: ''
      },
      formLabelWidth: '120px',
      dialogFormVisible: false,
      corpusFormVisible: false
    }
  },
  created () {
    // 获取收藏夹
    GetFolder({})
      .then(res => {
        this.folders = res
        console.log(this.folders)
        const parsedFolder = JSON.stringify(this.folders)
        localStorage.setItem('folders', parsedFolder)
      })

    // 获取词表库
    GetRepository({})
      .then(res => {
        this.repositorys = res
        console.log(this.repositorys)
        const parsedRepository = JSON.stringify(this.repositorys)
        localStorage.setItem('repositorys', parsedRepository)
      })

    // 获取页面数据
    GetSelectedFilterResult({
      target: JSON.stringify(this.selected)
    })
      .then(res => {
        this.result = res
        this.$message({
          type: 'success',
          message: '导入成功!'
        })

        // data in table 1
        let title = 'title'
        let author = 'author'
        let info = 'info'
        let date = 'date'
        var tableDict1 = { 'title': this.result[title], 'author': this.result[author], 'info': this.result[info], 'date': this.result[date] }
        this.tableData = Array(1).fill(tableDict1)
        console.log(this.result[author])

        // data in table 2
        let abstract = 'abstract'
        let source = 'source'
        var tableDict2 = { 'abstract': this.result[abstract], 'source': this.result[source] }
        this.detailData = Array(1).fill(tableDict2)

        // data in table 3
        let kws = 'kws'
        let fund = 'fund'
        let cited = 'cited'
        let downed = 'downed'
        var tableDict3 = { 'kws': this.result[kws], 'fund': this.result[fund], 'cited': this.result[cited], 'downed': this.result[downed] }
        this.otherData = Array(1).fill(tableDict3)
      })
      .catch(err => {
        console.log(err)
      })
  },
  mounted () {
    // 获取页面数据, 清除key
    if (localStorage.getItem('filterResult')) {
      this.filterResult = JSON.parse(localStorage.getItem('filterResult'))
      console.log(this.filterResult)
      localStorage.removeItem('filterResult')
    } else {
      console.log('No filterResult')
    }

    // 获取收藏夹, 清除key
    if (localStorage.getItem('folders')) {
      this.folders = JSON.parse(localStorage.getItem('folders'))
      console.log(this.folders)
      localStorage.removeItem('folders')
    } else {
      console.log('No folders')
    }

    // 获取词表库, 清除key
    if (localStorage.getItem('repositorys')) {
      this.repositorys = JSON.parse(localStorage.getItem('repositorys'))
      console.log(this.repositorys)
      localStorage.removeItem('repositorys')
    } else {
      console.log('No repositorys')
    }
  },
  methods: {
    addCollection (dialogFormVisible) {
      AddCollection({
        collect: JSON.stringify(this.tableData),
        flag: JSON.stringify(this.selected),
        folder: JSON.stringify(this.collectform.folder)
      })
        .then(res => {
          var feedback = res
          if (feedback === 'success') {
            this.$message({
              type: 'success',
              message: '收藏成功!'
            })
          } else if (feedback === 'failed') {
            this.$message({
              type: 'info',
              message: '论文已存在!'
            })
          }
          this.dialogFormVisible = false
        })
    },
    addCorpus (corpusFormVisible) {
      AppendCorpus({
        corpus: JSON.stringify(this.selectedItems),
        repository: JSON.stringify(this.corpusform.repository)
      })
        .then(res => {
          var feedback = res
          if (feedback === 'success') {
            this.$message({
              type: 'success',
              message: '收藏成功!'
            })
          } else if (feedback === 'failed') {
            this.$message({
              type: 'info',
              message: '词汇已存在!'
            })
          }
          this.corpusFormVisible = false
        })
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
      this.$router.push({
        name: 'detailsearch',
        params: {
          storage: this.filterResult // 传输页面数据
        }
      })
    }
  }
}
</script>
