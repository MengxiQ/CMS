<template>
  <div style="position: relative">
    <el-button class="tabs-btns" size="mini" type="success" @click.native.stop="getList">刷新</el-button>
    <el-tabs active-name="list">
      <el-tab-pane label="基本路由表" name="list" lazy>
        <el-table v-loading="loadingInit" :data="list">
          <el-table-column prop="prefix" label="网段" />
          <el-table-column prop="protocolId" label="协议" />
          <el-table-column prop="processId" label="协议ID" />
          <el-table-column prop="maskLength" label="掩码" />
          <el-table-column prop="ifName" label="出接口" />
          <el-table-column prop="directNexthop" label="下一跳" />
          <el-table-column prop="state" label="状态">
            <template slot-scope="props">
              <i v-if="isActiveRoute(props.row.state)" class="el-icon-success" style="color: rgb(103,194,58)" />
              <i v-else class="el-icon-error" style="color: red" />
              <span style="font-size: smaller">{{ props.row.state }}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="统计信息" name="rmStatistics" lazy>
        <rm-statistics v-loading="loadingInit" :rm-statistics="rmStatistics" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getRouteTable } from '@/api/detail/route/table'
import RmStatistics from '@/views/equipmentsManage/detail/components/configuration/components/route/table/rmStatistics'

export default {
  name: 'Table',
  components: { RmStatistics },
  mixins: [baseMinxin],
  data() {
    return {
      rmStatistics: null // 统计信息
    }
  },
  methods: {
    isActiveRoute(val) {
      if (val.match('Active')) {
        return true
      }
      if (val.match('Inactive')) {
        return false
      }
      return val
    },
    getList() {
      this.loadingInit = true
      getRouteTable(this.ip).then(res => {
        this.loadingInit = false
        this.list = res.data.rm.rmbase.uniAfs.uniAf.topologys.topology.routes.route
        this.rmStatistics = res.data.rm.rmbase.uniAfs.uniAf.topologys.topology.rmStatisticss.rmStatistics
      }).catch(error => this.getListError(error))
    }
  }

}
</script>

<style scoped>
  .tabs-btns {
    position: absolute;
    right: 20px;
    top: 3px;
    z-index: 1000;
  }
</style>
