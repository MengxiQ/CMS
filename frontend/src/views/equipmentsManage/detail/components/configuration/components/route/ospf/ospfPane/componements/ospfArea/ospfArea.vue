<template>
  <div>
    <el-divider content-position="left">
      OSPF区域
      <el-link title="新建" size="mini" type="primary" class="el-icon-edit" style="margin-left: 10px" @click="handleCreate"></el-link>
      <el-link title="刷新" class="el-icon-refresh" size="mini" type="success" style="margin-left: 10px" @click="getList" />
    </el-divider>
    <el-table
      v-loading="loadingInit"
      :data="list"
      highlight-current-row
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <ospf-area-networks :process-id="processId" :area-id="props.row.areaId"></ospf-area-networks>
          <ospf-area-interfaces :list="areainterfas(props.row)"></ospf-area-interfaces>
        </template>
      </el-table-column>
      <config-table :params="params"></config-table>
<!--      <el-table-column label="区域ID" prop="areaId" />-->
<!--      <el-table-column label="区域类型" prop="areaType" />-->
<!--      <el-table-column label="区域描述" prop="descriptionArea" />-->
<!--      <el-table-column label="认证模式" prop="authenticationMode" />-->
<!--      <el-table-column label="网络数">-->
<!--        <template slot-scope="scope">-->
<!--          {{ scope.row.networks?(isArray(scope.row.networks.network) ? scope.row.networks.network.length: 1): 0 }}-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column label="接口数">-->
<!--        <template slot-scope="scope">-->
<!--          {{ scope.row.interfaces?(isArray(scope.row.interfaces.interfaces) ? scope.row.interfaces.interfaces.length: 1): 0 }}-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column label="操作" prop="" width="150px" align="">
        <template slot-scope="scope">
          <el-button-group>
            <el-button type="" size="mini" icon="el-icon-edit" @click="handleUpdate(scope.row)" />
            <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(scope.row)" />
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
import { getOspfArea, createOspfArea, deleteOspfArea } from '@/api/detail/route/ospf/ospfArea'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'
import OspfAreaNetworks
  from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfPane/componements/ospfArea/ospfAreaNetworks'
import OspfAreaInterfaces
  from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfPane/componements/ospfArea/ospfAreaInterfaces'
import { isArray } from '@/utils/isType'
import ConfigTable from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/config-table'
export default {
  name: 'OspfArea',
  components: { ConfigTable, OspfAreaInterfaces, OspfAreaNetworks, Edit },
  mixins: [baseMinxin],
  props: {
    processId: {
      type: String
    }
  },
  created() {
    this.getList()
  },
  methods: {
    areainterfas(row) {
      const list = ((row || {}).interfaces || {}).interface
      if (list !== undefined) {
        return this.isArray(list) ? list : Array(list)
      } else return []
    },
    disparams() {
      // // 不要计算属性，因为缓存不需要动态改变
      if (this.dialogEditStatus === 'update') {
        // 如果为编辑模式，则下列字段为不可修改
        return ['processId', 'areaId']
      } else return ['processId']
    },
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        this.temp.processId = this.processId
        return this.temp
      } else return { processId: this.processId }
    },
    handleSave(temp) {
      // 创建区域
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createOspfArea(data).then(res => {
        this.$message({ type: 'success', message: '配置成功。' })
        this.$emit('complete')
        this.getList()
        this.dialogEditShow = false
      }).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      data.data.processId = this.processId
      deleteOspfArea(data).then(res => this.deleteSuccess()).catch(error => this.deleteError(error))
    },
    getList() {
      const query = {
        ip: this.ip,
        source: this.$store.getters.source,
        data: {
          processId: this.processId
        }
      }
      this.loadingInit = true
      getOspfArea(query).then(res => {
        const data = res.data ? res.data : []
        this.list = isArray(data) ? data : Array(data)
        this.params = res.params
        this.dataSource = query.source
        this.loadingInit = false
        // this.params = res.params
        // const list = (((((((res || {}).data || {}).ospfv2 || {}).ospfv2comm || {}).ospfSites || {}).ospfSite || {}).areas || {}).area
        // if (list !== undefined) {
        //   this.list = this.isArray(list) ? list : Array(list)
        // } else this.list = []
        // this.loadingInit = false
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>

</style>
