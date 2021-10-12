<!--
 * @Author: caojing
 * @Date: 2018-11-23 10:28:53
 * @LastEditors: weilixing
 * @LastEditTime: 2020-11-27 10:12:26
 -->
<template>
  <div class="shapebarWrap">
    <div class="shapebarHead" style="position: relative">
      设备列表
      <el-button
        v-if="shapeNodeLstData.length > 0"
        class="manage-btn"
        type="danger"
        size="mini"
        @click.stop.prevent="isManage = !isManage"
      >
        {{ isManage ? '隐藏' : '管理' }}
      </el-button>
      <el-popover
        v-model="selectEquipmentVisible"
        placement="right"
        trigger="click"
        width="600"
        title="添加设备"
      >
        <div class="select-equipment-contair">
          <!-- 添加设备-->
          <query-equipment @selected="selected"></query-equipment>
          <el-button style="float: right; margin-right: 5px" size="mini" @click="selectEquipmentVisible = false">关闭</el-button>
        </div>
        <el-button
          slot="reference"
          type="primary"
          class="manage-btn"
          size="mini"
        >
          添加
        </el-button>
      </el-popover>
    </div>
    <div class="shapeNodeLstWrap" style="position: relative">
      <!--      切换显示按钮 el-icon-s-fold / el-icon-menu -->
      <el-button
        title="切换显示方式"
        :icon="itemShowType ? 'el-icon-menu':'el-icon-s-fold'"
        circle
        size="mini"
        class="manage-btn"
        style="position: absolute; right: -2px;top: -7px;z-index: 100"
        @click.stop.prevent="itemShowType = !itemShowType"
      />

      <!--      显示方式：图标-->
      <ul v-if="itemShowType" class="shapeNodeLst">
        <li
          v-for="(ele,key) in shapeNodeLstData"
          :key="key"
          class="shapeNode"
          :title="ele.name"
          @mousedown.stop.prevent="dragShapeNode(shapeNodeLstData,key,$event)"
        >
          <div class="shapeIcon">
<!--            <img class="shapeIconImg" :src="ele.icon">-->
            <img class="shapeIconImg" src="@/assets/topo/switch.svg">
          </div>
          <div class="shapeName">{{ ele.name }}</div>
          <i v-if="isManage" class="el-icon-delete delete-btn" title="删除" @click.stop.prevent="deleteNode(key)"/>
        </li>
      </ul>
      <!--      显示方式：列表-->
      <ul v-else class="shapeNodeLst">
        <li
          v-for="(ele,key) in shapeNodeLstData"
          :key="key"
          class="shapeNode-list"
          :title="ele.name"
          @mousedown.stop.prevent="dragShapeNode(shapeNodeLstData,key,$event)"
        >
          <div class="shapeIcon-list">
            <img class="shapeIconImgi-list" src="@/assets/topo/switch.svg">
          </div>
          <div class="shapeName-list">{{ ele.name }}</div>
          <div class="shapeName-list" style="color: #3a8ee6">{{ ele.ip }}</div>
          <div class="shapeName-list">{{ ele.netype }}</div>

          <i v-if="isManage" class="el-icon-delete delete-btn" title="删除" @click.stop.prevent="deleteNode(key)"/>
        </li>
      </ul>
      <p style="color: #909399; padding: 50px 0px;text-align: left;">tips：del键--删除节点或者连线。</p>
    </div>
  </div>
</template>

<script>
// import shapeNodeLstData from '../../../data/toolbarNodeData' // 初始左侧toolbarNode数据（可从后台获取）
import QueryEquipment from '@/components/vuetopo/vTopo/components/vShapebar/components/queryEquipments'

export default {
  name: 'VShapebar',
  components: { QueryEquipment },
  props: {
    shapeNodeLstData: {
      type: Array
    }
  },
  data() {
    return {
      selectEquipmentVisible: false,
      itemShowType: true,
      // shapeNodeLstData: [], // shapebar数据
      isManage: false
    }
  },
  mounted() {
    // this.initToolbarNodes() //初始化toolbarNodes数据
  },
  created() {
  },
  methods: {
    // 时间，选择并返回的设备列表
    selected(data) {
      const shapeNodeLstData = data.map((item, key) => {
        return {
          type: 'switch',
          name: item.name,
          icon: '@/assets/topo/application.png',
          width: 50,
          height: 50,
          num: 1,
          classType: 'T2',
          ip: item.ip,
          netype: item.type.name,
          status: 'health'
          // status: 'alarm'
        }
      })
      this.$emit('selected', shapeNodeLstData)
    },
    // 多选
    handleSelectionChange() {
      console.log('handleSelectionChange')
    },
    dragShapeNode(shapeNodeLstData, key, $event) {
      this.$emit('click', shapeNodeLstData, key, $event)
    },
    // 初始shapeLstData
    initToolbarNodes() {
      let initShapeLstData = this.shapeNodeLstData // toolbarNodeData从后台获取
      if (!(initShapeLstData instanceof Array)) { // 类型检测，必须为Array
        console.error('shapeNodeLstData must be Array')
        initShapeLstData = []
      }
      this.shapeNodeLstData = initShapeLstData
    },

    // 删除节点
    deleteNode(key) {
      this.shapeNodeLstData.splice(key, 1)
    }
  }
}
</script>
<style lang="less" scoped>
@theme-color: rgb(245, 247, 250);
@theme-border-color: #aaaaaa;
@theme-font-color: #525252;
@border-color: #aaaaaa;
/*svgMain左侧工具栏*/
.manage-btn {
  float: right;
  margin-top: 7px;
  transform: scale(0.8)
}

.shapebarWrap {
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: 250px;
  border: 1px solid @border-color;
  border-right: 0;
  background: white;

  .shapebarHead {
    height: 40px;
    line-height: 40px;
    padding: 0 20px;
    text-align: left;
    font-size: 14px;
    -webkit-user-select: none;
    user-select: none;
    font-weight: 700;
    color: @theme-font-color;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    //border-bottom: 1px  solid @border-color;
    box-shadow: rgba(0, 0, 0, 0.2) 0 1px;
  }

  .shapeNodeLstWrap {
    overflow-y: auto;
    box-sizing: border-box;
    padding: 10px 15px;
    flex: 1;

    .shapeNodeLst {
      width: 100%;
      display: flex;
      flex-wrap: wrap;
      box-sizing: border-box;

    }
  }
}

.shapeNode {
  position: relative;
  margin-top: 5px;
  cursor: pointer;
  border: 1px solid #c7d1dd;
  border-radius: 2px;
  -webkit-user-select: none;
  user-select: none;
  background-color: #fff;
  -webkit-user-select: none;
  user-select: none;
  box-sizing: border-box;
  width: calc(~"( 100% - 10px ) / 3");
  box-sizing: border-box;
  padding: 6px 0;
  margin-right: 5px;

  &:nth-child(3n) {
    margin-right: 0
  }
}

.shapeNode-list {
  position: relative;
  margin-top: 5px;
  cursor: pointer;
  padding: 2px 5px;
  -webkit-user-select: none;
  user-select: none;
  //background-color: #fff;
  -webkit-user-select: none;
  user-select: none;
  width: 100%;
  box-sizing: border-box;
  display: block;
  text-align: left;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  //background: rebeccapurple;

}

.shapeNode-list:hover {
  background: #e4f1ff;
}

/*移动的node*/
.shapeIcon {
  text-align: center;
  -webkit-user-select: none;
  user-select: none;
}

.shapeIcon-list {
  text-align: center;
  -webkit-user-select: none;
  user-select: none;
  display: inline-block;
}

.shapeIconImg {
  width: 28px;
  height: 28px;
  -webkit-user-select: none;
  user-select: none;
}

.shapeIconImgi-list {
  width: 20px;
  height: 20px;
  -webkit-user-select: none;
  user-select: none;
  display: inline-block;
}

.shapeName {
  font-size: 12px;
  text-align: center;
  padding: 0 5px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  -webkit-user-select: none;
  user-select: none;
  color: #000
}

.shapeName-list {
  font-size: 12px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  -webkit-user-select: none;
  user-select: none;
  color: #000;
  display: inline-block;
  margin-left: 2px;
}

.delete-btn {
  color: red;
  position: absolute;
  top: 2px;
  right: 2px;
}

.delete-btn:hover {
  font-weight: bold;
}
</style>
