<template>
  <div v-loading="loadingInit">
    <divider-info :data-source="dataSource"/>
    <el-table :data="isArray(list) ? list : Array(list)">
      <el-table-column label="协议" prop="importProtocol"></el-table-column>
      <el-table-column label="协议ID" prop="importProcessId"></el-table-column>
      <el-table-column label="开销" prop="med"></el-table-column>
      <el-table-column label="操作" prop="" width="150">
        <template slot="header">
          <el-button-group>
            <el-button size="mini" type="primary" @click="handleCreate">新建</el-button>
            <el-button size="mini" type="success" @click="getList">刷新</el-button>
          </el-button-group>
        </template>
        <template slot-scope="scope">
          <el-button-group>
            <el-button size="mini" type="" @click="handleUpdate(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <!--编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow" :before-close="beforCloseDialog">
      <edit :params="params" :default_temp="defaultTemp()" :disparams="disparams()" @save="handleSave" @cancel="dialogEditShow = false" />
    </el-dialog>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getBgpImportProtocol, createBgpImportProtocol, deleteBgpImportProtocol } from '@/api/detail/route/bgp/bgp-base'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'

export default {
  name: 'BgpImportProtocol',
  components: { Edit, DividerInfo },
  mixins: [baseMinxin],
  methods: {
    disparams() {
      // // 不要计算属性，因为缓存不需要动态改变
      if (this.dialogEditStatus === 'update') {
        // 如果为编辑模式，则下列字段为不可修改
        return ['importProtocol', 'importProcessId']
      } else return []
    },
    handleSave(temp) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createBgpImportProtocol(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      deleteBgpImportProtocol(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getBgpImportProtocol(query).then(res => {
        // console.log(res)
        this.list = (((((((((res.data || {}).bgp || {}).bgpcomm || {}).bgpVrfs || {}).bgpVrf || {}).bgpVrfAFs || {}).bgpVrfAF || {}).importRoutes || {})).importRoute
        this.list = this.list === undefined ? [] : this.list
        this.getListSuccess(res, query)
      }).catch(error => this.getListError(error))
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
