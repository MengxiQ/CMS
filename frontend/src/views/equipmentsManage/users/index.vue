<template>
  <div class="content">
    <div class="heard-tool">
      <el-button-group>
        <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleAdd">添加</el-button>
        <el-button size="mini" type="success" icon="el-icon-refresh" @click="getList">刷新</el-button>
      </el-button-group>
    </div>
    <el-table
      v-loading="loading"
      :data="list"
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column
        type="index"
        width="50"
      />
      <el-table-column label="用户名" prop="username" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.username }}</span>
          <el-input v-else v-model="scope.row.username" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="密码" prop="password" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.password }}</span>
          <el-input v-else v-model="scope.row.password" type="" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="端口号" prop="port" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.port }}</span>
          <el-input v-else v-model="scope.row.port" type="" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="设备厂商" prop="device_params" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.device_params }}</span>
          <el-select v-else v-model="scope.row.device_params" type="" size="mini">
            <el-option label="华为" value="huawei" />
<!--            <el-option label="锐捷" value="ruijie" />-->
<!--            <el-option label="思科" value="cisco" />-->
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="设备IP" prop="equipment" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.networkequipment }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140" align="center">
        <template slot-scope="scope">
          <el-button-group>
            <el-button v-if="scope.row.enableEdit" size="mini" type="primary" @click="handleSave(scope.row)">保存
            </el-button>
            <el-button
              v-if="!scope.row.enableEdit"
              size="mini"
              style="margin-right: 5px"
              @click="scope.row.enableEdit = !scope.row.enableEdit"
            >编辑
            </el-button>
            <el-button
              v-else
              size="mini"
              @click="scope.row.enableEdit = !scope.row.enableEdit"
            >取消
            </el-button>
            <el-popconfirm
              v-if="!scope.row.enableEdit"
              title="确定删除吗？"
              @onConfirm="handleDelete(scope.row.id)"
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
    <!--    添加弹出框-->
    <el-dialog
      title="添加用户"
      :visible.sync="flags.addDialogVisible"
      width="50%"
      :before-close="beforeClose"
    >
      <el-form label-position="left" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="temp.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="temp.password" />
        </el-form-item><el-form-item label="端口号">
          <el-input v-model="temp.port" />
        </el-form-item>
        <el-form-item label="厂商">
          <el-select v-model="temp.device_params" style="">
            <el-option label="华为" value="huawei" />
            <el-option label="锐捷" value="ruijie" />
            <el-option label="思科" value="cisco" />
          </el-select>
        </el-form-item>
        <el-form-item label="设备IP">
          <el-input v-model="temp.networkequipment" />
        </el-form-item>
        <!--        <el-form-item label="HostKey">-->
        <!--          <el-input-->
        <!--            v-model="temp.hostkey"-->
        <!--            placeholder="请输入HostKey"-->
        <!--            type="textarea"-->
        <!--            :autosize="{ minRows: 5, }"-->
        <!--          />-->
        <!--        </el-form-item>-->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="beforeClose">取 消</el-button>
        <el-button type="primary" @click="commitAddData">确 定</el-button>
      </div>
    </el-dialog>

    <!--    编辑HostKey-->
    <!--    <el-dialog title="编辑" :visible="ShowEditHostKey" width="80%" @close="ShowEditHostKey = false">-->
    <!--      &lt;!&ndash;      <h1 style="position:absolute; margin: 0;padding: 0;width: 100%;text-align: left;font-size: 17px;font-weight: normal;height: 20px">{{ativeTemplate.name}}</h1>&ndash;&gt;-->
    <!--      <template slot="title">编辑HostKey: <span style="font-weight: bold; color: #3d7ed5">{{ activeItem.username }}</span></template>-->
    <!--      <el-input v-model="activeItem.hostkey" placeholder="请输入HostKey" type="textarea" :autosize="{ minRows: 5, }" />-->
    <!--      <div slot="footer" class="dialog-footer">-->
    <!--        <el-button size="mini" @click="ShowEditHostKey = false">-->
    <!--          取消-->
    <!--        </el-button>-->
    <!--        <el-button size="mini" type="primary" @click="saveHostKey">-->
    <!--          保存-->
    <!--        </el-button>-->
    <!--      </div>-->
    <!--    </el-dialog>-->
  </div>
</template>

<script>
import { fetchList, updateNetconfuser, createNetconfuser, deleteNetconfuser } from '@/api/netconfUsers'

export default {
  name: 'TemplateTypes',
  data() {
    return {
      query: { // 查询的过滤条件
        // name: ''
      },
      loading: true,
      list: [],
      activeItem: {},
      ShowEditHostKey: false,
      flags: {
        addDialogVisible: false
      },
      temp: {
        'id': 1,
        'equipment': '',
        'username': '',
        'password': '',
        'port': 22,
        'device_params': 'huawei',
        'networkequipment': ''
      }
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    showHostKey(row) {
      this.activeItem = row
      this.ShowEditHostKey = true
    },
    saveHostKey() {
      this.handleSave(this.activeItem)
    },
    beforeClose() {
      this.flags.addDialogVisible = false
      this.temp = {
        'id': 1,
        'equipment': '',
        'username': '',
        'password': '',
        'port': 22,
        'device_params': 'huawei',
        'networkequipment': ''
      }
    },
    handleAdd() {
      this.flags.addDialogVisible = true
    },
    commitAddData() {
      createNetconfuser(this.temp).then(res => {
        this.$message({ type: 'success', message: '添加成功，' })
        this.beforeClose()
        this.getList()
      }).catch(error => {
        console.log(error)
        this.$message({ type: 'error', message: '添加失败！' })
      })
    },
    handleCloseAddDialog() {

    },
    handleSave(row) {
      console.log(row)
      updateNetconfuser(row).then(res => {
        this.$message({ type: 'success', message: '保存成功，' })
        this.beforeClose()
        this.getList()
      }).catch(error => {
        console.log(error)
        // this.$message({ type: 'error', message: '保存失败！' })
        const data = error.response['data']
        this.$message({ type: 'error', message: '保存失败，' + data['msg'] })
        this.getList()
      })
    },
    handleDelete(id) {
      deleteNetconfuser(id).then(res => {
        this.$message({ type: 'success', message: '删除成功！' })
        this.getList()
      }).catch(erro => {
        this.$message({ type: 'error', message: '删除失败！' })
      })
    },
    getList() {
      this.loading = true
      fetchList(this.query).then(res => {
        // enableEdit
        const data = res.map(item => {
          item.enableEdit = false
          return item
        })
        this.list = data
        this.loading = false
      }).catch(erro => {
        console.log(erro)
        this.$message({ type: 'error', message: '获取列表失败！' })
      })
    }
  }
}
</script>

<style scoped>
  .heard-tool {
    padding: 10px;
  }
  .content {
    padding: 20px;
  }

</style>
