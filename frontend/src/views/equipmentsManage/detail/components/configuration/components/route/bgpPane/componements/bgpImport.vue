<template>
  <el-tabs type="border-card">
    <el-tab-pane>
      <span slot="label"><i class="el-icon-s-finance"></i>协议</span>
      <keep-alive>
        <bgp-import-protocol :ip="ip" />
      </keep-alive>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import BgpImportProtocol from '@/views/equipmentsManage/detail/components/configuration/components/route/bgpPane/componements/bgpImportProtocol'
// import BgpImportInstance from '@/views/equipmentsManage/detail/components/bgpPane/componements/bgpImportInstance'

export default {
  name: 'BgpImport',
  components: { BgpImportProtocol },
  props: {
    ip: {
      type: String
    }
  }
}
</script>

<style scoped>

.label-h5 {
  display: block;
  border-left: solid #3d7ed5 4px;
  padding: 3px 8px;
  margin: 10px 0;
}

</style>
