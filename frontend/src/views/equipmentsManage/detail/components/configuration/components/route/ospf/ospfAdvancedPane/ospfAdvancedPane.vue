<template>
  <div v-loading="loadingInit">
    <el-button style="position: absolute; z-index: 1000; right: 10px; top: 10px" icon="el-icon-refresh" type="success" size="mini" @click="getList">刷新</el-button>
    <divider-info :data-source="dataSource" />
    <el-table
      v-if="list"
      :data="isArray(list)?list:Array(list)"
      highlight-current-row
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <div class="inner-table">
            <ospf-import :process-id="props.row.processId"></ospf-import>
            <default-advisement :process-id="props.row.processId" :ip="ip" :list="Array((((props.row.ProcessTopologys || {}).ProcessTopology || {}).defaultRouteMTs || {}).defaultRouteMT)" @success="updateAdvisementSuccess" />
          </div>
        </template>
      </el-table-column>
      <el-table-column label="进程ID" prop="processId" />
      <el-table-column label="默认开销" prop="ProcessTopologys.ProcessTopology.defaultCost" />
      <el-table-column label="默认类型" prop="ProcessTopologys.ProcessTopology.defaultType" />
      <el-table-column label="topo名称" prop="ProcessTopologys.ProcessTopology.topoName" />
    </el-table>

  </div>
</template>

<script>
import { getOspfAdvance, createOspfAdvance, deleteOspfAdvance } from '@/api/detail/route/ospf/ospfAdvance/ospfAdvance'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import DefaultAdvisement from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfAdvancedPane/defaultAdvisement'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'
import OspfImport
  from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfAdvancedPane/ospfImport/ospfImport'

export default {
  name: 'OspfAdvancedPane',
  components: { OspfImport, DividerInfo, DefaultAdvisement },
  mixins: [baseMinxin],
  data() {
    return {}
  },
  methods: {
    updateAdvisementSuccess() {
      this.getList()
    },
    handleCreate(row) {
      this.temp = {}
      this.temp.processId = row.processId
      // console.log(this.temp)
      this.dialogEditStatus = 'create'
      this.dialogEditShow = true
    },
    handleUpdate(row, prow) {
      this.temp = row
      this.temp.processId = prow.processId
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getOspfAdvance(query).then(res => {
        // console.log(res)
        if (res.data) {
          this.list = res.data
          // if (this.isArray(res.data.ospfv2.ospfv2comm.ospfSites.ospfSite)) {
          //   this.list = res.data.ospfv2.ospfv2comm.ospfSites.ospfSite
          // } else {
          //   this.list = Array(res.data.ospfv2.ospfv2comm.ospfSites.ospfSite)
          // }
        }
        this.getListSuccess(res, query)
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>
.label-h5 {
  border-left: solid #3d7ed5 4px;
  padding-left: 4px;
  font-size: larger;
}

.inner-table {
  /*background: rgb(249, 249, 249);*/
  /*padding: 10px 10px 40px;*/
}
</style>
