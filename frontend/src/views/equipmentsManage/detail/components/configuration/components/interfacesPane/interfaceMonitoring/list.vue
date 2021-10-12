<template>
  <div>
    <el-button type="success" size="mini" @click="getList">刷新</el-button>
    <el-table v-loading="loadingInit" :data="list">
      <el-table-column  type="expand">
        <template scope="props">
          <el-link type="primary" class="el-icon-refresh" @click="chartKey += 1">重新渲染</el-link>
          <if-statistics :if-name="props.row.ifName" :key="chartKey" :if-statistics="props.row.ifStatistics"></if-statistics>
        </template>
      </el-table-column>
      <el-table-column label="名称" prop="ifName" />
<!--      <el-table-column label="类型" prop="ifPhyType" />-->
      <el-table-column label="物理状态" prop="ifDynamicInfo.ifPhyStatus" />
      <el-table-column label="链路状态" prop="ifDynamicInfo.ifLinkStatus" />
      <el-table-column label="运行状态" prop="ifDynamicInfo.ifOperStatus" />
      <el-table-column label="带宽" prop="ifDynamicInfo.ifOperSpeed">
        <template scope="props">
          <span>{{ parseInt(props.row.ifDynamicInfo.ifOperSpeed) / 1000000 + 'M' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="ifV4State" prop="ifDynamicInfo.ifV4State" />
      <el-table-column label="ifV6State" prop="ifDynamicInfo.ifV6State" />
      <el-table-column label="动态MTU" prop="ifDynamicInfo.ifOpertMTU" />
      <el-table-column label="生效MAC" prop="ifDynamicInfo.ifOperMac" />
      <el-table-column label="开启时间" prop="ifDynamicInfo.lineProtocolUpTime">
        <template scope="props">
          <span>{{ parseTime(props.row.ifDynamicInfo.lineProtocolUpTime) }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getInterfaceMonitoring } from '@/api/detail/interfaces'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import IfStatistics
  from '@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/interfaceMonitoring/ifStatistics'
export default {
  name: 'InterfaceList',
  components: { IfStatistics },
  mixins: [baseMinxin],
  data() {
    return {
      chartKey: 0
    }
  },
  methods: {
    getList() {
      this.loadingInit = false
      const query = {
        ip: this.ip
      }
      getInterfaceMonitoring(query).then(res => {
        this.list = res.data.ifm.interfaces.interface
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>

</style>
