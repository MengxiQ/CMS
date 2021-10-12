<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-button-group>
          <el-button title="创建" size="mini" type="primary" icon="el-icon-plus" @click="handleCreate"></el-button>
          <el-button title="刷新" size="mini" type="success" icon="el-icon-refresh" @click="getList"></el-button>
        </el-button-group>
      </el-col>
    </el-row>
    <el-table
      :data="list"
      max-height="200px"
      v-loading="loadingInit"
    >
      <el-table-column
        type="index"
        align="center"
      >
        <template slot="header"><i class="el-icon-view"></i>
        </template>
      </el-table-column>
      <el-table-column label="接口名称" align="center" prop="memberIfName"></el-table-column>
      <el-table-column label="带宽" align="center" prop="weight"></el-table-column>
      <el-table-column label="状态" align="center" prop="memberIfState">
        <template scope="props">
          <el-tag style="min-width: 50px" size="mini" :type="props.row.memberIfState === 'Up' ? 'success' : 'warning'">{{ props.row.memberIfState }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" prop="" width="150">
        <template slot-scope="scope">
          <el-button-group>
            <el-button icon="el-icon-edit" size="mini" type="" @click="handleUpdate(scope.row)"></el-button>
            <el-button icon="el-icon-delete" size="mini" type="danger" @click="handleDelete(scope.row)"></el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow">
      <edit :params="params" :default_temp="defaultTemp()" :disparams="['ifName']" @save="handleSave" @cancel="dialogEditShow = false"/>
    </el-dialog>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { createTrunkMember, deleteTrunkMember, getEthTrunkMember } from '@/api/detail/interfaces'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'

export default {
  name: 'TrunkMemberIf',
  components: { Edit },
  mixins: [baseMinxin],
  props: {
    ifName: {
      type: String
    }
  },
  methods: {
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        return this.temp
      } else return { ifName: this.ifName }
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        data: {
          ifName: this.ifName
        }
      }
      getEthTrunkMember(query).then(res => {
        this.params = res.params
        const list = (((((res.data || {}).ifmtrunk || {}).TrunkIfs || {}).TrunkIf || {}).TrunkMemberIfs || {}).TrunkMemberIf
        this.list = list === undefined ? [] : (this.isArray(list) ? list : Array(list))
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.temp.ifName = this.ifName
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    handleCreate() {
      this.temp.ifName = this.ifName
      this.dialogEditStatus = 'create'
      this.dialogEditShow = true
    },
    handleSave(temp) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createTrunkMember(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      data.data.ifName = this.ifName
      deleteTrunkMember(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    }

  }
}
</script>

<style scoped>

</style>
