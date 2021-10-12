<template>
  <div>
    <el-divider content-position="left">
      路由引入
      <el-link title="添加" type="primary" style="margin-left: 10px" class="el-icon-edit" @click="handleCreate"></el-link>
      <el-link title="刷新" type="success" style="margin-left: 10px" size="mini" icon="el-icon-refresh" @click="getList"/>
    </el-divider>
    <el-table :data="list" v-loading="loadingInit">
      <el-table-column label="协议" prop="protocol" />
      <el-table-column label="进程ID" prop="protocolProcessId" />
      <el-table-column label="开销" prop="cost" />
<!--      <el-table-column label="tag" prop="tag" />-->
<!--      <el-table-column label="type" prop="type" />-->
      <el-table-column label="管理" prop="adminStatus" width="150" align="center">
        <template slot-scope="scope">
<!--          <el-button size="mini" type="" @click="handleUpdate(scope.row)">编辑</el-button>-->
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--    编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow">
      <edit :params="params" :default_temp="defaultTemp()" :disparams="['processId']" @save="handleSave" @cancel="dialogEditShow = false" />
    </el-dialog>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getOspfAdvanceImport, createOspfAdvanceImport, deleteOspfAdvanceImport } from '@/api/detail/route/ospf/ospfAdvance/ospfAdvanceImport'
import { createOspfAdvance, deleteOspfAdvance, getOspfAdvance } from '@/api/detail/route/ospf/ospfAdvance/ospfAdvance'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'

export default {
  name: 'OspfImport',
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
      getOspfAdvanceImport(query).then(res => {
        this.params = res.params
        const data = res.data
        // 判断数据是否为空
        if (res.data) {
          this.list = this.isArray(data) ? data : Array(data)
          // const list = (res.data.ospfv2.ospfv2comm.ospfSites.ospfSite.ProcessTopologys.ProcessTopology.importRouteMTs || {}).importRouteMT
          // if (list !== undefined) {
          //   this.list = this.isArray(list) ? list : Array(list)
          // } else this.list = []
        }
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    },
    handleSave(temp) {
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createOspfAdvanceImport(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.temp = row
      this.temp.processId = this.processId
      const data = {
        ip: this.ip,
        data: this.temp,
        source: this.$store.getters.source
      }
      deleteOspfAdvanceImport(data).then(res => this.deleteSuccess()).catch(error => this.deleteError(error))
    }
  }
}
</script>

<style scoped>

</style>
