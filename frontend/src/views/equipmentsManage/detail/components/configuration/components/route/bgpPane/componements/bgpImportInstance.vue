<template>
  <div v-loading="loadingInit">
<!--    <h5 class="label-h5">引入实例路由-->
<!--      <el-link style="margin-left: 10px" type="primary" @click="handleCreate">新建</el-link>-->
<!--      <el-button style="float: right" size="mini" type="success" @click="getList">刷新</el-button>-->
<!--    </h5>-->
    <el-button size="mini" type="primary" @click="handleCreate"> 新建</el-button>
    <el-button size="mini" type="success" @click="getList">刷新</el-button>
    <divider-info :data-source="dataSource"/>
    <el-table :data="isArray(list) ? list : Array(list)">
      <el-table-column label="协议" prop="importProtocol"></el-table-column>
      <el-table-column label="协议ID" prop="importProcessId"></el-table-column>
      <el-table-column label="路由策略" prop="importRoutePolicy"></el-table-column>
      <el-table-column label="med" prop="med"></el-table-column>
      <el-table-column label="操作" prop="" width="150">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="handleUpdate(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow" :before-close="beforCloseDialog">
      <el-form label-position="left" label-width="140px">
        <el-form-item
          v-for="(item, key) in params"
          :key="key"
          style="position: relative; padding: 10px 0 20px 0"
          :label="item.name"
          size="medium"
        >
          <div style="position: absolute;z-index: 100;top: -28px; font-size: smaller; color: #5a5e66">{{ item.remark }}
            <span style="margin-left: 5px;color: #3d7ed5">({{ item.constraint }})</span></div>
          <el-select
            v-if="(item.constraint).match('CHIOCE<(?<p>.*)>')"
            v-model="temp[item.name]"
            :disabled="temp.l2Enable === 'disable' && item.name === 'linkType'"
          >
            <el-option
              v-for="(i, k) in constraint(item.constraint)"
              :key="k"
              :value="i"
              :label="i"
            />
          </el-select>
          <el-input
            v-if="item.constraint === 'INT' || item.constraint === 'IP' || item.constraint === 'MASK' || item.constraint === 'WILDCARD' || item.constraint === 'STRING'"
            v-model="temp[item.name]"
            :disabled="item.name === 'asNumber'"
          />
        </el-form-item>
      </el-form>
      <el-row>
        <el-col :span="24" style="text-align: right">
          <el-button type="primary" size="mini" @click="handleSave()">保存</el-button>
          <el-button type="" size="mini" @click="dialogEditShow = !dialogEditShow">取消</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getBgpImportInstance, createBgpImportInstance, deleteBgpImportInstance } from '@/api/detail/route/bgp/bgp-base'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'

export default {
  name: 'BgpImportInstance',
  components: { DividerInfo },
  mixins: [baseMinxin],
  methods: {
    handleSave() {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: this.temp,
        source: this.$store.getters.source
      }
      createBgpImportInstance(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDelete(row) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: row,
        source: this.$store.getters.source
      }
      deleteBgpImportInstance(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getBgpImportInstance(query).then(res => {
        // console.log(res)
        // this.params = res.params
        this.list = ((((((((res.data || {}).bgp || {}).bgpcomm || {}).bgpVrfs || {}).bgpVrf || {}).bgpVrfAFs || {}).bgpVrfAF || {}).importRoutes || {}).importRoute
        this.list = this.list === undefined ? [] : this.list
        // this.loadingInit = false
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
