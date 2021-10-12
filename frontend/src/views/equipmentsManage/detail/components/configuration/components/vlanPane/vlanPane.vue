<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-button-group>
          <el-button size="mini" type="primary" @click="handleCreate">添加</el-button>
          <el-button size="mini" type="success" @click="getList">刷新</el-button>
        </el-button-group>
      </el-col>

      <el-col style="padding-bottom: 100px">
        <divider-info :data-source="dataSource" />
        <el-table v-loading="loadingInit" :data="list">
          <el-table-column type="index">
            <template slot="header"><i class="el-icon-view" /></template>
          </el-table-column>
          <config-table :params="params"></config-table>
<!--          <el-table-column label="vlanId" prop="vlanId" />-->
<!--          <el-table-column label="名称" prop="vlanName" />-->
<!--          <el-table-column label="描述" prop="vlanDesc" />-->
<!--          <el-table-column label="类型" prop="vlanType" />-->
<!--          <el-table-column label="管理" prop="adminStatus">-->
<!--            <template slot-scope="scope">-->
<!--              <el-tag size="mini" :type="scope.row.adminStatus === 'up'?'success':'danger'">-->
<!--                {{ scope.row.adminStatus }}-->
<!--              </el-tag>-->
<!--            </template>-->
<!--          </el-table-column>-->
          <el-table-column label="操作" prop="adminStatus" width="150">
            <template slot-scope="scope">
              <el-button-group>
                <el-button size="mini" type="primay" @click="handleUpdate(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <!--    编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow">
      <edit :params="params" :default_temp="defaultTemp()" :disparams="disparams()" @save="handleSave" @cancel="dialogEditShow = false" />
    </el-dialog>
  </div>
</template>

<script>
import { getVlans, createVlans, deleteVlans } from '@/api/detail/vlans'
import { isArray } from '@/utils/isType'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import ConfigTable from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/config-table'
export default {
  name: 'VlanPane',
  components: { ConfigTable, Edit, DividerInfo },
  mixins: [baseMinxin],
  props: {
  },
  data() {
    return {
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: '编辑VLAN',
        create: '创建VLAN'
      }
    }
  },
  computed: {
    ip() {
      return this.$route.params.ip
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    disparams() {
      // 不要计算属性，因为缓存不需要动态改变
      if (this.dialogEditStatus === 'update') {
        // 如果为编辑模式，则下列字段为不可修改
        return ['vlanId']
      } else return []
    },
    handleDelete(row) {
      console.log(row)
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      deleteVlans(data).then(res => {
        this.$message({ type: 'success', message: '删除成功。' })
        this.getList()
      }).catch(error => {
        console.log(error)
        if (error.response) {
          const data = error.response['data']
          this.$message({ type: 'error', message: data['msg'] })
        } else {
          this.$message({ type: 'error', message: '获取列表失败.' })
        }
      })
    },
    handleSave(temp) {
      // 因为更新和创建的方法是一样的所以只需要一个方法
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      this.loadingInit = true
      createVlans(data).then(res => {
        this.$message({ type: 'success', message: '配置成功' })
        this.temp = {}
        this.dialogEditShow = false
        this.getList()
      }).catch(error => {
        const data = error.response['data']
        this.$message({ type: 'error', message: data['msg'] })
        this.loadingInit = false
      })
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getVlans(query).then(res => {
        // if (isArray(res.data.vlan.vlans.vlan)) {
        //   this.list = res.data.vlan.vlans.vlan
        // } else {
        //   this.list = Array(res.data.vlan.vlans.vlan)
        // }
        const data = res.data ? res.data : []
        this.list = isArray(data) ? data : Array(data)
        this.params = res.params
        this.dataSource = query.source
        this.loadingInit = false
        // this.temp = Object.assign({}, this.params[0])
      }).catch(error => {
        // console.log(error.response)
        if (((error.response || {}).data || {}).msg) {
          const data = error.response.data
          this.params = data.params
          // 候选数据没有创建
          console.log(data.msg)
          if (data.msg.match('candidate data store does not exist.') !== null) {
            this.list = []
            this.dataSource = this.$store.getters.source
            this.$message({ type: 'info', message: '开始配置并创建candidate数据库.' })
          } else {
            this.$message({ type: 'error', message: data.msg })
          }
        } else {
          this.$message({ type: 'error', message: '获取列表失败.' })
        }
        // print('candidate data store does not exist.')
        this.loadingInit = false
      })
    }
  }
}
</script>

<style scoped>

</style>
