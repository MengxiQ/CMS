<template>
  <div>
    <el-table :data="list" v-loading="loadingInit">
      <el-table-column label="网段" prop="networkAddress" />
      <el-table-column label="掩码长度" prop="maskLen" />
<!--      <el-table-column label="策略名称" prop="networkPolicy" />-->
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
      <edit :params="params" :default_temp="defaultTemp()" :disparams="['asNumber']" @save="handleSave" @cancel="dialogEditShow = false" />
    </el-dialog>
  </div>
</template>

<script>
import { createBgpNetwork, deleteBgpNetwork, getNetworkPeer } from '@/api/detail/route/bgp/bgp-base'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'

export default {
  name: 'BgpNetwork',
  components: { Edit },
  mixins: [baseMinxin],
  props: {
    asNumber: {
      type: String
    }
  },
  methods: {
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        this.temp.asNumber = this.asNumber
        return this.temp
      } else return { asNumber: this.asNumber }
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source,
        data: {
          asNumber: this.asNumber
        }
      }
      getNetworkPeer(query).then(res => {
        this.params = res.params
        if (res.data !== null) {
          const list = (((((res.data.bgp.bgpcomm.bgpVrfs || {}).bgpVrf || {}).bgpVrfAFs || {}).bgpVrfAF || {}).networkRoutes || {}).networkRoute
          this.list = this.isArray(list) ? list : Array(list)
        } else this.list = []
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
      createBgpNetwork(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.loadingInit = true
      row.asNumber = this.asNumber
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      deleteBgpNetwork(data).then(res => this.createSuccess()).catch(error => this.createError(error))
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
