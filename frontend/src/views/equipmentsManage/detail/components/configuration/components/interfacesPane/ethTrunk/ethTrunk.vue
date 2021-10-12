<template xmlns:edit="http://www.w3.org/1999/html">
  <div v-loading="loadingInit">
    <el-button-group>
      <el-button type="primary" size="mini" @click="handleCreate">添加</el-button>
      <el-button type="success" size="mini" @click="getList">刷新</el-button>
    </el-button-group>
    <divider-info :data-source="dataSource" />
    <el-table :data="isArray(list) ? list : Array(list)" highlight-current-row>
      <el-table-column type="expand">
        <template slot="header"><i class="el-icon-view" /></template>
        <template slot-scope="scope">
<!--          :params="menmberParams"-->
<!--              -->
<!--              :list="scope.row.TrunkMemberIfs ?(isArray(scope.row.TrunkMemberIfs.TrunkMemberIf) ? scope.row.TrunkMemberIfs.TrunkMemberIf : Array(scope.row.TrunkMemberIfs.TrunkMemberIf)):[]"-->
<!--              @createsuccess="getList"-->
          <div style="background-color: #f9f9f9; padding: 10px">
            <trunk-member-if :ip="ip" :if-name="scope.row.ifName" />
          </div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="名称" prop="ifName" />
      <el-table-column align="center" label="最小活动数" prop="minUpNum" />
      <el-table-column align="center" label="最大活动数" prop="maxUpNum" />
      <el-table-column align="center" label="工作模式" prop="workMode" />
<!--      <el-table-column align="center" label="MAC" prop="ifMac" width="130" />-->
      <el-table-column align="center" label="接口类型" prop="trunkType" />
      <el-table-column align="center" label="操作" prop="" width="150">
        <template slot-scope="scope">
          <el-button-group>
            <el-button size="mini" type="" @click="handleUpdate(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <!-- 编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow" :before-close="beforCloseDialog">
      <edit :params="params" :default_temp="temp" @save="handleSave" @cancel="dialogEditShow = false"></edit>
    </el-dialog>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import {
  getEthTrunkInterfaces,
  createEthTrunkInterface,
  deleteEthTrunkInterface
} from '@/api/detail/interfaces'
import TrunkMemberIf from '@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/ethTrunk/trunkMemberIf'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'

export default {
  name: 'EthTrunk',
  components: { Edit, DividerInfo, TrunkMemberIf },
  mixins: [baseMinxin],
  data() {
    return {
      menmberParams: []
    }
  },
  methods: {
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getEthTrunkInterfaces(query).then(res => {
        // this.list = ((((res.data || {}).ifmtrunk || {}).TrunkIfs || {}).TrunkIf) || []
        const data = res.data
        if (data !== null) {
          this.list = data
        }
        this.getListSuccess(res, query)
      }).catch(error => this.getListError(error))
    },
    handleSave(temp) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createEthTrunkInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      deleteEthTrunkInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
      console.log('delete', data)
    }
  }
}
</script>

<style scoped>

</style>
