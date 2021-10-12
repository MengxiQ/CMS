<template>
  <div v-loading="loadingInit">
    <el-button-group>
      <el-button type="primary" size="mini" @click="handleCreate">添加</el-button>
      <el-button type="success" size="mini" @click="getList">刷新</el-button>
    </el-button-group>
    <divider-info :data-source="dataSource" />
    <el-table
      v-loading="loadingInit"
      :data="list"
    >
      <el-table-column label="状态" width="100" prop="ifAdminStatus" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.ifAdminStatus === 'up'" class="el-icon-success" style="color: #67C23A" />
          <span v-else class="el-icon-error" style="color: #F56C6C" />
        </template>
      </el-table-column>
      <el-table-column
        label="名称"
        prop="ifName"
        align="center"
      />
      <el-table-column
        label="MAC"
        prop="ifMac"
        align="center"
      />
      <el-table-column
        label="类型"
        prop="isL2SwitchPort"
        align="center"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.isL2SwitchPort === 'true'" size="" type="">二层</el-tag>
          <el-tag v-else size="" type="success">三层</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="IPv4" align="center">
        <template slot-scope="props">
          <span>{{ props.row.ipv4Config.am4CfgAddrs ? props.row.ipv4Config.am4CfgAddrs.am4CfgAddr.ifIpAddr : '' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Mask" align="center">
        <template slot-scope="props">
          <span>{{ props.row.ipv4Config.am4CfgAddrs ? props.row.ipv4Config.am4CfgAddrs.am4CfgAddr.subnetMask : '' }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="描述"
        prop="ifDescr"
        align="center"
      />
      <el-table-column label="操作" align="center" width="150">
        <template slot-scope="scope">
          <!--          <el-button v-if="scope.row.ifAdminStatus === 'down'" type="primary" size="mini">-->
          <!--            打开-->
          <!--          </el-button>-->
          <!--          <el-button v-else type="danger" size="mini">-->
          <!--            关闭-->
          <!--          </el-button>-->
          <el-button type="" size="mini" @click="handleUpdate(scope.row)">
            编辑
          </el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--    编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible="dialogEditShow" :before-close="beforCloseDialog">
      <el-form label-position="left" label-width="120px">
        <el-form-item
          v-for="(item, key) in params"
          :key="key"
          style="position: relative; padding: 10px 0 20px 0"
          :label="item.name"
          size="medium"
        >
          <div style="position: absolute;z-index: 100;top: -28px; font-size: smaller; color: #5a5e66">{{ item.remark }}
            <span style="margin-left: 5px;color: #3d7ed5">({{ item.constraint }})</span></div>
          <el-radio-group size="mini" v-if="(item.constraint).match('CHIOCE<(?<p>.*)>')" v-model="temp[item.name]">
            <el-radio-button
              v-for="(i, k) in constraint(item.constraint)"
              :key="k"
              :value="i"
              :label="i"
            />
          </el-radio-group>
          <el-input
            v-if="item.constraint === 'INT' || item.constraint === 'IP' || item.constraint === 'MASK' || item.constraint === 'WILDCARD' || item.constraint === 'STRING'"
            v-model="temp[item.name]"
            :disabled="temp.l2Enable === 'enable' && (item.name === 'ifIpAddr'|| item.name === 'subnetMask')"
          />
        </el-form-item>
      </el-form>
      <el-row>
        <el-col :span="24" style="text-align: right">
          <el-button type="primary" size="mini" @click="handleSave()">保存</el-button>
          <el-button type="" size="mini" @click="beforCloseDialog">取消</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {
  getCommonInterfaces,
  createCommonInterface,
  deleteCommonInterface
} from '@/api/detail/interfaces'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'

export default {
  name: 'CommonInterfaces',
  components: { DividerInfo },
  mixins: [baseMinxin],
  props: {},
  data() {
    return {
      temp: {
        ifName: '',
        ifIpAddr: '',
        subnetMask: '',
        ifDescr: '',
        l2Enable: '',
        isL2SwitchPort: '',
        ifAdminStatus: '',
      },
      odltemp: {},
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: '编辑接口',
        create: '创建接口'
      }
    }
  },
  methods: {
    beforCloseDialog() {
      this.dialogEditShow = false
      this.temp = {
        ifName: '',
        ifIpAddr: '',
        subnetMask: '',
        ifDescr: '',
        l2Enable: '',
        isL2SwitchPort: '',
        ifAdminStatus: ''
      }
    },
    handleDelete(row) {
      const data = {
        ip: this.ip,
        data: row,
        operation: 'delete-interface'
      }
      // console.log(data)
      this.loadingInit = true
      deleteCommonInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleUpdate(row) {
      this.dialogEditStatus = 'update'
      this.temp.ifAdminStatus = row.ifAdminStatus
      this.temp.ifName = row.ifName
      this.temp.ifDescr = row.ifDescr
      this.temp.isL2SwitchPort = row.isL2SwitchPort
      // isL2SwitchPort 是true ，那么l2Enable 就是enable
      this.temp.l2Enable = String((row.isL2SwitchPort === 'true' ? 'enable' : 'disable'))
      if (row.ipv4Config.am4CfgAddrs) {
        this.temp.ifIpAddr = String(row.ipv4Config.am4CfgAddrs.am4CfgAddr.ifIpAddr)
        this.temp.subnetMask = String(row.ipv4Config.am4CfgAddrs.am4CfgAddr.subnetMask)
      }
      this.dialogEditShow = true
      // console.log(this.temp)
      this.odltemp = Object.assign({}, this.temp)
    },
    handleSave() {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: this.temp,
        source: this.$store.getters.source
      }
      const odldata = {
        ip: this.ip,
        data: this.odltemp,
        source: this.$store.getters.source
      }
      if (this.dialogEditStatus === 'update') {
        // update
        // 1 删除
        // console.log('odldata', this.odltemp)
        if (this.odltemp.ifIpAddr === '') {
          console.log('空，直接创建')
          createCommonInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
        } else {
          console.log('非空，先删除再创建')
          deleteCommonInterface(odldata).then(res => {
            // 2 创建
            console.log('删除成功')
            // 如果（没有输入地址） 则直接返回成功  //this.temp.l2Enable === 'enable')
            if (this.temp.ifIpAddr === '') {
              this.createSuccess()
            } else {
              createCommonInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
            }
          }).catch(error => this.createError(error))
        }
      } else {
        // create
        createCommonInterface(data).then(res => this.createSuccess()).catch(error => this.createError(error))
      }
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getCommonInterfaces(query).then(res => {
        // console.log(res)
        // this.list = res.data.ifm.interfaces.interface
        this.list = res.data
        this.params = res.params
        this.dataSource = query.source
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    }
  }
}
</script>
<style scoped>
.label-h5 {
  border-left: solid #3d7ed5 4px;
  padding-left: 4px;
  font-size: 15px;
}

.expand {
  background-color: #f9f9f9;
  padding: 5px;
}
</style>
