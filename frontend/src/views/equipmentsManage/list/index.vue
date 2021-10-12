<template>
  <div class="app-container">
    <el-button-group style="float: left">
      <el-button size="small" class="filter-item" style="" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加
      </el-button>
      <!--      <el-button v-waves size="small" :loading="downloadLoading" class="filter-item" type="primary"-->
      <!--                 icon="el-icon-download" @click="handleDownload">-->
      <!--        导出-->
      <!--      </el-button>-->
      <el-button size="small" class="filter-item" style="" type="success" icon="el-icon-refresh" @click="getList">刷新
      </el-button>
    </el-button-group>
    <div style="float: right">
      <el-input
        v-model="listQuery.name"
        size="small"
        placeholder="设备名称"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      <el-input
        v-model="listQuery.ip"
        size="small"
        placeholder="IP地址"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
      />
      <el-select v-model="listQuery.type" size="small" placeholder="类型" clearable class="filter-item">
        <el-option v-for="(item, key) in this.$store.getters.neTypes" :key="key" :label="item.name" :value="item.id" />
      </el-select>
      <el-button v-waves size="small" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜素
      </el-button>
    </div>
    <el-table
      v-loading="loadingInit"
      :data="list"
    >
      <el-table-column type="index">
        <template slot="header"><i class="el-icon-view" /></template>
      </el-table-column>
      <el-table-column label="名称" prop="name" />
      <el-table-column label="IP地址" prop="ip" align="" width="140">
        <template slot-scope="{row}">
          <span><el-link type="primary" @click="gotoDetail(row)">{{ row.ip }}</el-link></span>
        </template>
      </el-table-column>
      <el-table-column label="型号" prop="unittype.name" align="" />
      <el-table-column label="设备类型" prop="type.name" align="" />
      <el-table-column label="添加日期" align="">
        <template slot-scope="{row}">
          <span>{{ parseTime(new Date(Date.parse(row.stock_date))) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户" align="">
        <template slot-scope="{row}">
          <el-button v-if="row.user === null" size="mini" type="danger" @click="handleCreateUser(row)">添加</el-button>
          <el-button v-else size="mini" @click="handleUpdateUser(row)">编辑</el-button>
        </template>
      </el-table-column>
      <el-table-column label="状态" class-name="status-col" align="">
        <template slot-scope="{row}">
          <el-tag :type="(row.status ? row.status.type.show_type : null)">
            {{ row.status ? row.status.type.name : '无状态' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="" width="150" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button-group>
            <el-button type="" size="mini" @click="handleUpdate(row)">编辑</el-button>
<!--            <el-button size="mini" type="danger" @click="handleDelete(row,$index)">删除-->
<!--            </el-button>-->
            <el-popconfirm
              title="确定删除吗？"
              @onConfirm="handleDelete(row,$index)"
            >
              <el-button
                slot="reference"
                size="mini"
                type="danger"
              >删除
              </el-button>
            </el-popconfirm>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <!--    分页-->
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
    <!--    编辑设备-弹出编辑框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible="dialogEditShow" width="50%" :before-close="handleCloseDialog">
      <el-form size="" label-position="left" label-width="80px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="temp.type" placeholder="Please select">
            <el-option v-for="(item, key) in this.$store.getters.neTypes" :key="key" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="型号" prop="unittype">
          <el-select v-model="temp.unittype">
            <el-option
              v-for="(item,key) in this.$store.getters.unitTypes"
              :key="key"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="IP" prop="ip">
          <el-input v-model="temp.ip" />
        </el-form-item>
        <el-form-item label="创建时间" prop="stock_date">
          <el-date-picker v-model="temp.stock_date" disabled type="datetime" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="temp.remark" type="textarea" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="handleCloseDialog">取消</el-button>
        <el-button type="primary" @click="dialogEditStatus==='create'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
    <!--编辑用户-->
    <el-dialog
      :title="user_textMap[user_dialogEditStatus]"
      :visible="addUserDialogVisible"
      width="50%"
      :before-close="handleCloseDialogUser"
    >
      <el-form label-position="left" label-width="80px">
        <el-form-item label="设备IP">
          <el-input v-model="user_temp.networkequipment" disabled />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="user_temp.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="user_temp.password" />
        </el-form-item><el-form-item label="端口号">
          <el-input v-model="user_temp.port" />
        </el-form-item>
        <el-form-item label="厂商">
          <el-select v-model="user_temp.device_params" style="">
            <el-option label="华为" value="huawei" />
            <el-option label="huaweiyang" value="huaweiyang" />
            <el-option label="锐捷" value="ruijie" />
            <el-option label="思科" value="cisco" />
            <el-option label="default" value="default" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleCloseDialogUser">取 消</el-button>
        <el-button type="primary" @click="user_dialogEditStatus==='create'?createUserData():updateUserData()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import { deleteEquipment, fetchEquipmentList, updateEquipment, createEquipment } from '@/api/equipment'
import { createNetconfuser, updateNetconfuser } from '@/api/netconfUsers'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { commonOperationMixin } from '@/views/mixins/commonOperationMixin'
import { commonNetworkMixin } from '@/views/mixins/commonNetwork'
import { commonValidateMixin } from '@/views/mixins/commonValidateMixin'

export default {
  name: 'EquipmentList',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        '在线': 'success',
        '离线': 'danger'
        // draft: 'info',
      }
      return statusMap[status]
    }
  },
  mixins: [commonValidateMixin, commonNetworkMixin, commonOperationMixin],
  data() {
    return {
      // user:
      addUserDialogVisible: false,
      user_temp: {},
      user_dialogEditStatus: '',
      user_textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: '编辑用户',
        create: '添加用户'
      },
      // 设备列表：
      list: [],
      device_params: [
        { key: 'huawei', display_name: '华为' },
        { key: 'cisco', display_name: '思科' },
        { key: 'ruijie', display_name: '锐捷' }
      ],
      total: 0,
      listQuery: {
        page: 1,
        limit: 10,
        ip: undefined,
        name: undefined,
        type: undefined,
        sort: '+id'
      },
      temp: {
        ip: null,
        mac: null,
        stock_date: new Date(),
        status: null,
        name: '',
        type: null,
        unittype: '',
        remark: ''
      },
      restTemp: {
        ip: null,
        mac: null,
        stock_date: new Date(),
        status: null,
        name: '',
        type: null,
        unittype: '',
        remark: ''
      },
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: '编辑设备',
        create: '添加设备'
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    gotoDetail(row) {
      const statusType = ((row.status || {}).type || {}).name
      if (statusType === '离线' || statusType === undefined) {
        this.$message({ type: 'error', message: '该设备不在线！' })
      } else {
        const URL = this.$router.resolve({
          path: 'detail/' + row.ip + '/'
        })
        window.open(URL.href, '_blank')
        // this.$router.push({
        //   path: 'detail/' + row.ip + '/'
        // })
      }
    },
    getList() {
      this.loadingInit = true
      fetchEquipmentList(this.listQuery).then(response => {
        if (response !== null) {
          this.list = response.results
          this.total = response.count
        } else {
          this.list = []
          this.total = 0
        }
        this.loadingInit = false
      }).catch(error => {
        console.log(error)
        this.loadingInit = false
        this.$message({ type: 'error', message: '请求失败！' })
      })
    },
    handleCloseDialog() {
      this.beforeDialogClose(_ => {
        this.temp = Object.assign({}, this.restTemp)
        this.dialogEditShow = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreate() {
      this.temp = Object.assign({}, this.restTemp)
      this.dialogEditStatus = 'create'
      this.dialogEditShow = true
    },
    handleUpdate(row) {
      this.temp.id = row.id
      this.temp.ip = row.ip
      this.temp.name = row.name
      this.temp.unittype = row.unittype.id
      this.temp.type = row.type.id
      this.temp.remark = row.remark
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    handleDelete(row, index) {
      deleteEquipment(row).then(res => this.opsSuccess('删除')).catch(error => this.opsError(error, '删除'))
    },
    createData() {
      createEquipment(this.temp).then(res => this.opsSuccess('创建')).catch(error => this.opsError(error, '创建'))
    },
    updateData() {
      updateEquipment(this.temp).then(res => this.opsSuccess('更新')).catch(error => this.opsError(error, '更新'))
    },
    // user:
    handleCloseDialogUser() {
      this.beforeDialogClose(_ => {
        this.user_temp = Object.assign({}, {})
        this.addUserDialogVisible = false
      })
    },
    handleCreateUser(row) {
      this.user_temp = Object.assign({}, {})
      this.user_temp.networkequipment = row.ip
      this.user_dialogEditStatus = 'create'
      this.addUserDialogVisible = true
    },
    handleUpdateUser(row) {
      this.user_temp.networkequipment = row.networkequipment
      this.user_temp = Object.assign({}, row.user)
      this.user_temp.networkequipment = row.ip
      this.user_dialogEditStatus = 'update'
      this.addUserDialogVisible = true
    },
    createUserData() {
      this.loadingInit = true
      createNetconfuser(this.user_temp).then(res => this.opsSuccess('创建用户', _ => {
        this.addUserDialogVisible = false
        this.loadingInit = false
      })).catch(error => this.opsError(error, '创建用户', _ => {
        this.addUserDialogVisible = false
        this.loadingInit = false
      }))
    },
    updateUserData() {
      this.loadingInit = true
      updateNetconfuser(this.user_temp).then(res => this.opsSuccess('更新用户', _ => {
        this.addUserDialogVisible = false
        this.loadingInit = false
      })).catch(error => this.opsError(error, '更新用户', _ => {
        this.addUserDialogVisible = false
        this.loadingInit = false
      }))
    }
  }
}
</script>
<style lang="scss" scoped>
</style>
