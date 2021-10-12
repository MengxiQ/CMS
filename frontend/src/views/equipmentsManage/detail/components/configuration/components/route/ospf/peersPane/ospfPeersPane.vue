<template>
  <div>
    <el-button style="position: absolute; z-index: 1000; right: 10px; top: 10px" icon="el-icon-refresh" type="success" size="mini" @click="getList">刷新</el-button>
    <el-tabs v-loading="loadingInit" type="border-card">
      <el-tab-pane v-for="(item, key) in list" :key="key" :label="'进程' + item.processId">
        <el-table :data="item.neighbors ? (isArray(item.neighbors.neighbor) ? item.neighbors.neighbor : Array(item.neighbors.neighbor)) : []">
          <el-table-column label="区域ID" prop="areaId"/>
          <el-table-column label="接口" prop="ifName"/>
          <el-table-column label="邻居路由ID" prop="nbrRouterId"/>
          <el-table-column label="邻居地址" prop="nbrIpAddr"/>
          <el-table-column label="状态" prop="nbrState" >
            <template scope="props">
              <el-tag :type="props.row.nbrState === 'Full' ? 'success' : 'warning'">{{ props.row.nbrState }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getOspfPeersTable } from '@/api/detail/route/ospf/ospfPeersTable'
import { isArray } from '@/utils/validate'

export default {
  name: 'OspfPeersPane',
  mixins: [baseMinxin],
  methods: {
    isArray(o) {
      return isArray(o)
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getOspfPeersTable(query).then(res => {
        const result = (((res.data.ospfv2 || {}).ospfv2comm || {}).ospfSites || {}).ospfSite
        this.list = isArray(result) ? result : Array(result)
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>

</style>
