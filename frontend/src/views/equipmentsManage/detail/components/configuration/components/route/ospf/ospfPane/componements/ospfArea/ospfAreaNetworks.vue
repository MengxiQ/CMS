<template>
  <div v-loading="loadingInit">
    <el-divider content-position="left">
      Network
      <el-link title="新建" size="mini" type="primary" class="el-icon-edit" style="margin-left: 10px" @click="handleCreate"></el-link>
      <el-link title="刷新" type="success" class="el-icon-refresh" style="margin-left: 10px" @click="getList" />
    </el-divider>
    <!--  v-if="props.networks" // 如果区域没添加属性就False-->
    <el-table
      :data="list"
      style="border:1px rgb(235,238,245) solid"
    >
<!--      <el-table-column label="ipAddress" prop="ipAddress" />-->
<!--      <el-table-column label="wildcardMask" prop="wildcardMask" />-->
<!--      <el-table-column label="description" prop="description" />-->
      <config-table :params="params"></config-table>
      <el-table-column label="操作" prop="" width="150px" align="center">
        <template slot-scope="scope">
          <el-button-group>
            <el-button type="" size="mini" icon="el-icon-edit" @click="handleUpdate(scope.row)" />
            <el-button
              type="danger"
              size="mini"
              icon="el-icon-delete"
              @click="handleDelete(scope.row)"
            />
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <!-- 编辑区域对话框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow">
      <edit :params="params" :default_temp="defaultTemp()" :disparams="disparams()" @save="handleSave" @cancel="dialogEditShow = false" />
    </el-dialog>
  </div>
</template>

<script>
import { getOspfAreaNetwork, createOspfAreaNetwork, deleteOspfAreaNetwork } from '@/api/detail/route/ospf/ospfAreaNetwork'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'
import { isArray } from '@/utils/isType'
import ConfigTable from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/config-table'

export default {
  name: 'OspfAreaNetworks',
  components: { ConfigTable, Edit },
  mixins: [baseMinxin],
  props: {
    processId: {
      type: String
    },
    areaId: {
      type: String
    }
  },
  methods: {
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        this.temp.processId = this.processId
        this.temp.areaId = this.areaId
        return this.temp
      } else return { processId: this.processId, areaId: this.areaId }
    },
    disparams() {
      return ['processId', 'areaId']
      // // 不要计算属性，因为缓存不需要动态改变
      // if (this.dialogEditStatus === 'update') {
      //   // 如果为编辑模式，则下列字段为不可修改
      //   return ['prefix', 'maskLength', 'ifName', 'nexthop']
      // } else return []
    },
    handleSave(temp) {
      // 创建网络
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createOspfAreaNetwork(data).then(res => this.createSuccess()).catch(error => this.getListError(error))
    },
    handleDelete(row) {
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      data.data.processId = this.processId
      data.data.areaId = this.areaId
      deleteOspfAreaNetwork(data).then(res => this.createSuccess()).catch(error => this.getListError(error))
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        data: {
          processId: this.processId,
          areaId: this.areaId
        }
      }
      getOspfAreaNetwork(query).then(res => {
        // this.params = res.params
        // const list = (((((((((res || {}).data || {}).ospfv2 || {}).ospfv2comm || {}).ospfSites || {}).ospfSite || {}).areas || {}).area || {}).networks || {}).network
        // if (list !== undefined) {
        //   this.list = this.isArray(list) ? list : Array(list)
        // } else this.list = []
        // this.loadingInit = false
        const data = res.data ? res.data : []
        this.list = isArray(data) ? data : Array(data)
        this.params = res.params
        this.dataSource = query.source
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>

</style>
