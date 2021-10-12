<template>
  <div v-loading="loadingInit">
    <el-button-group>
      <el-button type="success" size="mini" @click="getList">刷新</el-button>
    </el-button-group>
    <divider-info :data-source="dataSource"></divider-info>
    <el-table
      :data="list"
    >
      <el-table-column
        type="index"
        align="center"
      >
        <template slot="header"><i class="el-icon-view" />
        </template>
      </el-table-column>
      <el-table-column
        label="名称"
        prop="ifName"
        align="center"
      />
      <el-table-column
        label="类型"
        prop="l2Enable"
        align="center"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.l2Enable === 'enable'" size="" type="">二层</el-tag>
          <el-tag v-else size="" type="success">三层</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="链路类型"
        prop="l2Attribute.linkType"
        align="center"
      />
      <el-table-column
        label="接口vlan"
        prop="l2Attribute.pvid"
        align="center"
      />
      <el-table-column
        label="TrunkVlan"
        prop=""
        align="center"
      >
        <template slot-scope="scope">
          <span style="max-width: 100px; max-height: 50px; display: block; overflow: hidden ">
            <span>{{ scope.row.l2Attribute ? vlans(scope.row.l2Attribute.trunkVlans) : '' }}</span>
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="150">
        <template slot-scope="scope">
          <el-button type="" size="mini" @click="handleUpdate(scope.row)">
            编辑
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--    编辑框-->
    <el-dialog width="90%" :title="dialogEditStatus" :visible.sync="dialogEditShow" :before-close="beforCloseDialog">
      <el-form label-position="left" label-width="120px">
        <el-form-item
          v-for="(item, key) in params"
          v-if="item.name !== 'trunkVlans'"
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
            v-if="(item.name !== 'trunkVlans') && (item.constraint === 'INT' || item.constraint === 'IP' || item.constraint === 'MASK' || item.constraint === 'WILDCARD' || item.constraint === 'STRING')"
            v-model="temp[item.name]"
            :disabled="temp.l2Enable === 'disable' && (item.name === 'linkType'|| item.name === 'pvid'|| item.name === 'trunkVlans'|| item.name === 'trunkVlans' )"
          />
        </el-form-item>
        <el-form-item label="trunkVlans">
          <el-select
            class="input-item"
            v-model="temp.trunkVlans"
            multiple
            filterable
            allow-create
            default-first-option
            clearable
          >
<!--            <el-option label="all" :value="all" />-->
          </el-select>
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
import { getEthernetInterfaces, createEthernetInterface } from '@/api/detail/interfaces'
import { isArray } from '@/utils/validate'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'

export default {
  name: 'EthernetInterfaces',
  components: { DividerInfo },
  filters: {
  },
  mixins: [baseMinxin],
  data() {
    return {
      all: [],
      temp: {
        ifName: '',
        l2Enable: '',
        linkType: '',
        pvid: '',
        trunkVlans: ''
      }
    }
  },
  computed: {},
  created() {
    for (let i = 1; i <= 4094; i++) {
      this.all.push(i)
    }
  },
  methods: {
    vlans(val) {
      if (isArray(val)) {
        if (JSON.stringify(val) === JSON.stringify(this.all)) {
          return 'all'
        } else {
          return val
        }
      } else {
        return null
      }
    },
    beforCloseDialog() {
      this.dialogEditShow = false
      this.temp = {
        ifName: '',
        l2Enable: '',
        linkType: '',
        pvid: '',
        trunkVlans: ''
      }
    },
    handleUpdate(row) {
      this.temp.ifName = row.ifName
      this.temp.l2Enable = row.l2Enable
      if (row.l2Attribute) {
        this.temp.linkType = row.l2Attribute.linkType
        this.temp.pvid = row.l2Attribute.pvid
        this.temp.oldTrunkVlans = row.l2Attribute.trunkVlans
        this.temp.trunkVlans = row.l2Attribute.trunkVlans
      }
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    createError(error) {
      // The interface is not a L2 interface
      const data = error.response['data']
      console.log(String(data['msg']).search('interface'))
      if (String(data['msg']).search('The interface is not a L2 interface.') === 0) {
        this.$message({ type: 'success', message: '切换到三层接口' })
        this.getList()
        this.dialogEditShow = false
      } else {
        this.$message({ dangerouslyUseHTMLString: true, type: 'error', message: ' 配置失败! <br><br>  提示信息:' + data['msg'] })
      }
      this.loadingInit = false
    },
    handleSave() {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: this.temp,
        source: this.$store.getters.source
      }
      // console.log(data)
      createEthernetInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    getList() {
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      this.loadingInit = true
      getEthernetInterfaces(query).then(res => {
        // console.log(res)
        // this.list = res.data.ethernet.ethernetIfs.ethernetIf
        this.list = res.data
        this.getListSuccess(res, query)
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>
  .input-item {
    width: 100%;
  }
</style>
