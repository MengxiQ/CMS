<template>
  <div class="topoArea">
    <!--    <p>拓扑信息：</p>-->
    <!--    <p>设备数量：0，异常：0 正常：0</p>-->
    <!--    {{this.$route.params}}-->
    <v-topo :editable="editable" :topo-data="topoData" />
  </div>
</template>

<script>
// import topoJson from '@/views/view/topos/detail/topoData2'
import VTopo from '@/components/vuetopo/vTopo/vTopo'

export default {
  name: 'Detail',
  components: { VTopo },
  props: {
    topoData: {
      type: Object,
      default() {
        return {
          'name': '',
          'nodes': [],
          'connectors': []
        }
      }
    },
    editable: {
      default() {
        return false
      }
    }
  },
  data: function() {
    return {
      isCanEdit: false,
      isShowEditDailog: true
      //       topoData: {
      //   'name': '666',
      //   'nodes': [{
      //     'name': '交换机4',
      //     'type': 'ApplicationModule',
      //     'ip': '192.168.0.100',
      //     'netype': '交换机',
      //     'id': '5t4va5c310c0',
      //     'x': 60,
      //     'y': 260,
      //     'icon':'data:image/png;base64,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',
      //     'width': 50,
      //     'height': 50,
      //     'initW': 50,
      //     'initH': 50,
      //     'classType': 'T2',
      //     'isLeftConnectShow': true,
      //     'isRightConnectShow': true,
      //     'containNodes': [],
      //     'attrs': [],
      //     'isSelect': false
      //   }],
      //   'connectors': []
      // },
      //   {
      //   'name': '',
      //   'nodes': [],
      //   'connectors': []
      // }
    }
  },
  computed: {
    // topoData(){
    //   console.log(this.$route.params['name'])
    //   return null
    // }
  }
}
</script>

<style type="less" scoped>
body {
  background: url('/src/assets/topo/canvas_bg.jpg');
}

#app {
  height: 100%
}

.topoArea {
  height: calc(100% - 70px);
  min-height: 800px;
  box-sizing: border-box;
}
</style>
