<template>
  <el-tabs>
    <el-tab-pane :lazy="true" label="基本配置">
      <ospf-pane :ip="ip" />
    </el-tab-pane>
    <el-tab-pane :lazy="true" label="高级配置">
      <ospf-advanced-pane :ip="ip" />
    </el-tab-pane>
    <el-tab-pane :lazy="true" label="邻居表">
      <ospf-peers-pane></ospf-peers-pane>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import OspfAdvancedPane from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfAdvancedPane/ospfAdvancedPane'
import OspfPane from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfPane/ospfPane'
import OspfPeersPane
  from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/peersPane/ospfPeersPane'
export default {
  components: { OspfPeersPane, OspfPane, OspfAdvancedPane},
  computed: {
    ip() {
      return this.$route.params.ip
    }
  }
}
</script>

<style scoped>

</style>
