<template>
  <div>
    <el-divider content-position="left">
      缺省路由发布
      <el-link title="添加" type="primary" style="margin-left: 10px" class="el-icon-edit" @click="handleCreate"></el-link>
      <el-link title="刷新" type="success" style="margin-left: 10px" size="mini" icon="el-icon-refresh" @click="getList"></el-link></el-divider>
    <el-table :data="list" v-loading="loadingInit">
      <el-table-column label="开启" prop="defRoutEnableFlag">
        <template slot-scope="props">
          <el-tag :type="props.row.defRoutEnableFlag === 'true' ? 'success' : 'danger'">{{ props.row.defRoutEnableFlag }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="方式" prop="flag" />
<!--      <el-table-column label="计算其他" prop="permitCalculateOther" />-->
      <el-table-column label="延迟时间" prop="delayTimer" />
      <el-table-column label="操作">
        <template slot-scope="props">
          <el-button size="mini" type="" @click="handleUpdate(props.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogEditStatus" :visible.sync="dialogEditShow" >
      <edit :params="params" :default_temp="defaultTemp()" :disparams="['processId']" @save="handleSave" @cancel="dialogEditShow = false"></edit>
    </el-dialog>
  </div>
</template>
<script>
import { getOspfDefaultAdvise, createOspfDefaultAdvise } from '@/api/detail/route/ospf/ospfAdvance/ospfAdvance'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'

export default {
  name: 'DefaultAdvisement',
  components: { Edit },
  mixins: [baseMinxin],
  props: {
    processId: { type: String }
  },
  methods: {
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        this.temp.processId = this.processId
        return this.temp
      } else return { processId: this.processId }
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source,
        data: {
          processId: this.processId
        }
      }
      getOspfDefaultAdvise(query).then(res => {
        this.params = res.params
        const data = res.data
        console.log(data)
        if (data) {
          // const list = res.data.ospfv2.ospfv2comm.ospfSites.ospfSite.ProcessTopologys.ProcessTopology.defaultRouteMTs.defaultRouteMT
          this.list = this.isArray(data) ? data : Array(data)
        }
        // if (data === null) {
        //   // 没有开启缺省路由发布
        //   this.list = [{ processId: this.processId, defRoutEnableFlag: 'false' }]
        // }
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    },
    handleSave(temp) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createOspfDefaultAdvise(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    }
  }
}
</script>

<style scoped>

</style>
