<!--
 * @Author: caojing
 * @Date: 2018-11-21 09:31:49
 * @LastEditors: caojing
 * @LastEditTime: 2018-11-23 14:43:14
 -->
<template>
  <div id="topoAttrWrap" :class="{active:isShowPanel}">
    <h3 id="topoAttrHeader">属性设置框</h3>
    <div v-if="JSON.stringify(nodeData)=='{}'" class="noAttrTip">
      未选择任何节点属性
    </div>
    <div v-else class="topoAttrBody">
      <div class="topoAttrMain">

        <el-form size="mini" :disabled="!editable" label-width="100px" class="demo-ruleForm" label-position="left">
          <div v-if="vSelectNodeData.type == 'Line'">
            <el-divider content-position="left"><span class="title">样式设置</span></el-divider>
            <el-form-item label="颜色选择">
              <el-color-picker v-model="vSelectNodeData.color" />
            </el-form-item>
            <el-form-item label="粗细选择">
              <el-slider
                v-model="vSelectNodeData.strokeW"
                :step="1"
                show-stops
                :min="3"
                :max="20"
              />
            </el-form-item>
            <el-divider content-position="left"><span class="title">连接设置</span> <el-link type="primary" :disabled="loading" @click="getList">采集</el-link></el-divider>
            <el-form size="mini" v-loading="loading" :disabled="!editable" label-position="top" style="text-align: left">
              <el-form-item :label="'目标接口('+vSelectNodeData.sourceNode.ip+')'">
                <el-select v-model="vSelectNodeData.sourceNode.port" placeholder="请选择">
                  <el-option
                    v-for="(item, key) in sourceNodeInterfaces"
                    :key="key"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </el-form-item>
              <el-form-item :label="'目标接口('+vSelectNodeData.targetNode.ip+')'">
                <el-select v-model="vSelectNodeData.targetNode.port" placeholder="请选择">
                  <el-option
                    v-for="(item, key) in targetNodeInterfaces"
                    :key="key"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </el-form-item>
            </el-form>
          </div>
          <div v-else>
            <el-form size="mini" :disabled="!editable" label-position="left" label-width="80px">
              <el-form-item label="节点名称">
                <el-input v-model="vSelectNodeData['name']" />
              </el-form-item>
               <el-form-item label="IP地址">
                <el-input v-model="vSelectNodeData['ip']" />
              </el-form-item>
<!--              <el-form-item label="图标">-->
<!--                <el-input v-model="vSelectNodeData['icon']" />-->
<!--              </el-form-item>-->
              <el-form-item label="节点类型">
                <el-input v-model="vSelectNodeData['type']" />
              </el-form-item>
<!--              <el-form-item label="图标类型">-->
<!--                <el-select  v-model="vSelectNodeData['classType']">-->
<!--                  <el-option label="T1 (容器)" value="T1" />-->
<!--                  <el-option label="T2 (节点)" value="T2" />-->
<!--                </el-select>-->
<!--              </el-form-item>-->
<!--              <el-form-item  label="图标高度">-->
<!--                <el-input v-model="vSelectNodeData['height']" />-->
<!--              </el-form-item>-->
<!--              <el-form-item  label="图标宽度">-->
<!--                <el-input v-model="vSelectNodeData['width']" />-->
<!--              </el-form-item>-->
            </el-form>
          </div>
        </el-form>
      </div>
<!--      <div class="topoAttrFooter">-->
<!--        &lt;!&ndash;                <nl-button type="primary" style="margin-right:15px;">确定</nl-button>&ndash;&gt;-->
<!--        &lt;!&ndash;                <nl-button>取消</nl-button>&ndash;&gt;-->
<!--        <el-button type="primary">确定</el-button>-->
<!--        <el-button type="">取消</el-button>-->
<!--      </div>-->
    </div>
    <i
      class="topoAttrArrow"
      :class="{'pushIcon':!isShowPanel,'pullIcon':isShowPanel}"
      @click="$emit('changeshow', !isShowPanel)"
    >
      <img v-if="!isShowPanel" src="@/assets/topo/push.svg">
      <img v-else src="@/assets/topo/pull.svg">
    </i>
  </div>
</template>

<script>
import { getEthernetInterfaces } from '@/api/detail/interfaces'

export default {
  name: 'VTopoAttrPanel',
  filters: {},
  components: {},
  props: {
    isShowPanel: {
      type: Boolean
    },
    editable: {
      type: Boolean
    },
    topoData: {
      type: Object,
      default: function() {
        return {}
      }
    },
    vSelectNodeData: {
      type: Object,
      default: function() {
        return {}
      }
    }
  },
  data() {
    return {
      isTopoAttrShow: false,
      sourceNodeInterfaces: [],
      targetNodeInterfaces: [],
      loading: false

    }
  },
  computed: {
    nodeData() {
      return JSON.parse(JSON.stringify(this.vSelectNodeData))
    }
  },
  mounted() {
  },
  created() {
  },
  methods: {
    node(id) {
      // 根据id查找到name
      // console.log('id：'+id)
      // console.log(this)
      let node = {}
      if (this !== undefined && this.topoData !== {} && this.topoData !== undefined) {
        this.topoData.nodes.forEach(item => {
          if (item.id === id) {
            // console.log(item.name)
            node = {
              name: item.name,
              ip: item.ip
            }
            return true
          }
        })
      }
      return node
    },
    getList() {
      this.loading = true
      const sip = this.vSelectNodeData.sourceNode.ip
      const tip = this.vSelectNodeData.targetNode.ip
      // console.log(sip, tip)
      const promiseArr = [
        getEthernetInterfaces(sip).then(res => {
          this.sourceNodeInterfaces = res.data.ethernet.ethernetIfs.ethernetIf.map(item => {
            return item.ifName
          })
        }),
        getEthernetInterfaces(tip).then(res => {
          this.targetNodeInterfaces = res.data.ethernet.ethernetIfs.ethernetIf.map(item => {
            return item.ifName
          })
        })
      ]
      Promise.all(promiseArr).then(res => {
        console.log(res)
        this.loading = false
        this.$message({ type: 'success', message: '获取接口列表成功.' })
      }).catch(error => {
        console.log(error)
        this.loading = false
        this.$message({ type: 'error', message: '获取接口列表失败.检查设备是否在线.' })
      })
    }
  }
}
</script>

<style lang="less">

</style>
<style lang="less" scoped>
@theme-color: rgb(245,247,250);
@theme-border-color: #aaaaaa;
@theme-font-color:#525252;
#topoAttrWrap {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 300px;
  position: absolute;
  top: 0;
  right: -400px;
  background: #fff;
  border-left: 1px solid darken(@theme-color, 10%);
  transition: all 1s;
  box-sizing: border-box;

  &.active {
    right: 0;
    box-shadow: -1px 0px 15px @theme-color
  }

  .topoAttrArrow {
    color: @theme-color;
    font-size: 20px;
    position: absolute;
    top: 50%;
    translate: transform(0 -50%);
    z-index: 200;
    cursor: pointer;

    &.pushIcon {
      left: -17px;
    }

    &.pullIcon {
      left: -2px;
    }
  }

  #topoAttrHeader {
    padding: 10px 0;
    background-color: darken(@theme-color, 5%);
    color: @theme-font-color;
    text-align: center;
    font-weight: 400;
    font-size: 14px;
  }

  .noAttrTip {
    padding: 50px;
    text-align: center;
    flex: 1;
  }

  .topoAttrBody {
    flex: 1;
    display: flex;
    flex-direction: column;

    .topoAttrMain {
      overflow-y: scroll;
      padding: 20px 15px;
      box-sizing: border-box;
    }

    .topoAttrFooter {
      padding: 30px 0;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
  .title {
   font-size: 15px;
    font-weight: ;
  }
}
</style>
