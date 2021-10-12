<template>
  <div v-loading="loadingInit">
    <el-row>
      <el-col :span="24">
        <el-button-group>
          <el-button size="mini" type="primary" @click="handleCreate">添加</el-button>
          <el-button size="mini" type="success" @click="getList">刷新</el-button>
        </el-button-group>
      </el-col>
    </el-row>
    <divider-info :data-source="dataSource" />
    <el-table :data="isArray(list) ? list : Array(list)">
      <!--      <el-table-column align="center" label="vrf" prop="vrfName" />-->
      <el-table-column align="center" label="网段" prop="prefix" width="120" />
      <el-table-column align="center" label="掩码长度" prop="maskLength" />
      <!--      <el-table-column align="center" label="目标vrf" prop="destVrfName" />-->
      <el-table-column align="center" label="出接口" prop="ifName" />
      <el-table-column align="center" label="下一跳" prop="nexthop" width="140" />
      <!--      <el-table-column align="center" label="tag" prop="tag" />-->
      <el-table-column align="center" label="描述" prop="description" />
      <el-table-column align="center" label="操作" prop="" width="150">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="handleUpdate(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--    编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow">
      <edit :params="params" :default_temp="defaultTemp()" :disparams="disparams()" @save="handleSave" @cancel="dialogEditShow = false"></edit>
    </el-dialog>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getSatic_route, createSatic_route, deleteSatic_route } from '@/api/detail/route/static_route'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'

export default {
  name: 'StaticRoutePane',
  components: { Edit, DividerInfo },
  mixins: [baseMinxin],
  data() {
    return {
      temp: {}
    }
  },
  methods: {
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        return this.temp
      } else return {}
    },
    disparams() {
      // 不要计算属性，因为缓存不需要动态改变
      if (this.dialogEditStatus === 'update') {
        // 如果为编辑模式，则下列字段为不可修改
        return ['prefix', 'maskLength', 'ifName', 'nexthop']
      } else return []
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getSatic_route(query).then(res => {
        // console.log(res)
        if (res.data) {
          this.list = res.data.staticrt.staticrtbase.srRoutes.srRoute
        } else {
          this.list = []
        }
        this.getListSuccess(res, query)
      }).catch(error => this.getListError(error))
    },
    handleSave(temp) {
      // 子组件返回 temp
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createSatic_route(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      deleteSatic_route(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    }
  }
}
</script>

<style scoped>

</style>
