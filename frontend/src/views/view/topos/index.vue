<template>
  <div v-loading="loadingInit" class="topos">
    <el-row>
      <el-col :span="4">
        <div v-if="!editable" >
          <h3 class="menu-title">
<!--            <el-button size="mini" type="" @click="addTopo">添加</el-button>-->
            <el-button-group>
              <el-button size="mini" type="" @click="isManage = !isManage">管理</el-button>
              <el-button icon="el-icon-refresh" type="success" size="mini" @click="getList"></el-button>
              <el-button size="mini" type="primary" @click="detailKey += 1">RS</el-button>
              </el-button-group>
          </h3>
          <ul class="menu">
            <li
              v-for="(item, key) in toppsList"
              :key="key"
              class="menu-item"
              :class="{'menu-item-active': key === isActive}"
              @click="gotoDetail(key)"
            >
              <i class="el-icon-s-marketing" style="margin-right: 5px" />{{ item.name }}
              <i v-show="isManage" class="el-icon-delete delete-item" @click="deleteItem(item)" />
            </li>
          </ul>
<!--          <el-button-->
<!--            v-show="isManage"-->
<!--            style="transform: scale(0.8)"-->
<!--            type="danger"-->
<!--            size="mini"-->
<!--            icon="el-icon-delete"-->
<!--          >删除-->
<!--          </el-button>-->
          <p style="font-size:12px; color: #6f7180; line-height: 18px; padding: 4px; font-family: '微软雅黑'">
            tips:<br>
            如果更新窗口后渲染异常，请尝试[RS]重新渲染topology。<br>
            选中多个设备ping只会ping第一选中的节点。
          </p>
        </div>
      </el-col>
      <el-col :span="rightSpan">
        <div class="right-contair">
          <div class="topo-title" :class="{'editableHeard':editable}">
            <span v-if="!editable">
              {{ this.toppsList[this.isActive] ? this.toppsList[this.isActive].name : '' }}
            </span>
            <el-button
              v-if="!editable"
              type=""
              size="mini"
              style="float: right; margin-right: 5px;margin-top: 1px; display: inline-block; transform: scale(0.9)"
              :disabled="toppsList[isActive] === undefined"
              @click="editable = ! editable"
            >编辑
            </el-button>
            <el-button
              v-if="editable"
              type=""
              size="mini"
              style="float: right; margin-right: 5px;margin-top: 1px; display: inline-block; transform: scale(0.9)"
              @click="updateTopo"
            >保存
            </el-button>
            <el-button
              v-if="editable"
              type=""
              size="mini"
              style="float: right; margin-right: 5px;margin-top: 1px; display: inline-block; transform: scale(0.9)"
              @click="handleCancle"
            >取消
            </el-button>
          </div>
          <Detail :key="detailKey" :topo-data="toppsList[isActive]" :editable="editable" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Detail from '@/views/view/topos/detail/index'
import { viewBaseMinxin } from '@/views/view/mixins/viewBaseMixin'
import { getTopologyList, updateTopology, deleteTopology } from '@/api/views/topology'

export default {
  name: 'Topos',
  components: { Detail },
  mixins: [viewBaseMinxin],
  proprs: {},
  data() {
    return {
      detailKey: 0,
      isManage: false,
      // activeTopo: {},
      // isActive: 0,
      editable: false
    }
  },
  computed: {
    rightSpan() {
      if (this.editable) {
        return 24
      } else {
        return 20
      }
    },
    isActive() {
      const key = this.$route.query['key']
      if (key === undefined) {
        return 0
      } else {
        return key
      }
    }
    // activeTopo() {
    //   const key = this.$route.query['key']
    //   console.log(key)
    //   return this.toppsList[key]
    // }
  },
  mounted() {
    // this.activeTopo = this.toppsList[this.isActive]
    this.$nextTick(_ => {
      setInterval(_ => {
        this.loadingInit = true
        getTopologyList().then(res => {
        // console.log(res)
          this.toppsList = res.map(item => {
            return {
              id: item.id,
              name: item.name,
              connectors: JSON.parse(item.connectors),
              nodes: JSON.parse(item.nodes)
            }
          })
          // this.activeTopo = this.toppsList[this.isActive]
          this.loadingInit = false
        }).catch(error => this.getListError(error))
        console.log('refresh Topotogy.', 'avtiveKey:', this.isActive)
      }, 10000000)
    })
  },
  methods: {
    handleCancle() {
      this.editable = false
      this.getList()
    },
    gotoDetail(key) {
      this.$router.push({ query: { key: key }})
      // this.activeTopo = this.toppsList[key]
    },
    addTopo() {
      this.$router.push('/view/edit')
    },
    getList() {
      this.loadingInit = true
      getTopologyList().then(res => {
        // console.log(res)
        this.toppsList = res.map(item => {
          return {
            id: item.id,
            name: item.name,
            connectors: JSON.parse(item.connectors),
            nodes: JSON.parse(item.nodes)
          }
        })
        // this.activeTopo = this.toppsList[0]
        // 重新渲染topo
        this.detailKey += 1
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    },
    deleteItem(item) {
      // 这里应该是commit
      // console.log(this.$store.state.toposData)
      // this.$store.state.toposData.splice(key,1)
      // this.$store.commit('deleteTopoItem', key)
      // this.$message({ type: 'success', message: '删除成功' })
      console.log(item)
      const data = {
        id: this.toppsList[this.isActive].id
        // name: this.activeTopo.name,
        // nodes: JSON.stringify(this.activeTopo.nodes),
        // connectors: JSON.stringify(this.activeTopo.connectors)
      }
      deleteTopology(data).then(res => this.opsSuccess('删除')).catch(error => this.opsError(error, '删除'))
    },
    opsSuccess(ops) {
      this.$message({ type: 'success', message: ops + '成功。' })
      this.getList()
      this.dialogEditShow = false
      this.loadingInit = false
      this.editable = false
    },
    updateTopo() {
      // console.log('update')
      const data = {
        id: this.toppsList[this.isActive].id,
        name: this.toppsList[this.isActive].name,
        nodes: JSON.stringify(this.toppsList[this.isActive].nodes),
        connectors: JSON.stringify(this.toppsList[this.isActive].connectors)
      }
      updateTopology(data).then(res => this.opsSuccess('更新')).catch(error => this.opsError(error, '更新'))
      // this.$store.commit('saveTopo', this.activeTopo)
      // this.$message({ type: 'success', message: '保存成功' })
      // this.editable = false
    }
  }
}
</script>

<style scoped>
ul, li {
  margin: 0;
  padding: 0;
  list-style: none;
}

.topos {
  width: 100%;
}

.left-contair {
  background: #fdfdfd;
  width: 100%;
  height: 100vh;
  border-right: rgba(0, 0, 0, 0.1) 1px solid;
}

.right-contair {
  background: white;
  width: 100%;
  height: 100vh;
  position: relative;
}

.menu-title {
  margin: 10px 0 10px 5px;
  font-size: 14px;
  line-height: 20px;
  background: #f3f3f3;
  color: #343740;
  border-left: rgb(48,65,86) 4px solid;

}

.menu-title {
  padding: 5px;
  position: relative;
}

.menu {
  width: 100%;
  /*height: 100px;*/

}

.menu-item {
  text-align: left;
  width: 100%;
  padding: 5px 5px 5px 20px;
  font-size: smaller;
  display: block;
}

.menu-item-active {
  background: #d6ebfc;
}

.menu-item:hover {
  background: #d6ebfc;
  cursor: pointer;
}

.menu-btn {
  transform: scale(0.8);
  margin: 0;
  position: absolute;
  top: 2px;
}

.delete-item {
  float: right;
  color: #ff0000;
  margin-right: 5px;
}

.delete-item:hover {
  /*transform: scale(1.1);*/
  font-weight: bold;
}

.topo-title {
  padding: 0;
  height: 30px;
  line-height: 30px;
  width: 100%;
  position: absolute;
  top: 0;
  z-index: 100;
  text-align: center;
  font-family:"Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  font-size: 14px;
  background: rgba(48,65,86,0.8);
  color: #f8f8f8;
}

.editableHeard {
  height: 28px;
  width: 200px;
  right: 2px;
  top: 2px;
  background: rgb(245, 247, 250);
  /*background: red;*/
}
</style>
