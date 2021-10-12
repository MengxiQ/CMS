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
    >
      <el-table-column
        type="index"
        width="50"
      >
        <template slot="header"><i class="el-icon-view"></i></template>
      </el-table-column>
      <el-table-column label="用户名" prop="username" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.username }}</span>
          <el-input v-else v-model="temp.username" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="密码" prop="password" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit" class="el-icon-view"></span>
          <el-input v-else v-model="temp.password" type="password" size="mini" placeholder="请输入新密码" show-password />
        </template>
      </el-table-column>
      <el-table-column label="邮箱" prop="email" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.email }}</span>
          <el-input v-else v-model="temp.email" type="" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="加入时间" prop="date_joined" align="center">
        <template slot-scope="scope">
          <span>{{ parseTime(new Date(Date.parse(scope.row.date_joined))) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="激活" prop="date_joined" align="center">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">
            <el-tag v-if="scope.row.is_active === true" type="success" size="mini">激活</el-tag>
            <el-tag v-else type="danger" size="mini">禁用</el-tag>
          </span>
          <el-switch
            v-else
            v-model="temp.is_active"
            active-color="#13ce66"
            inactive-color="#ff4949"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140" align="center">
        <template slot-scope="scope">
          <el-button-group>
          <el-button v-if="scope.row.enableEdit" size="mini" type="primary" @click="handleSave">保存</el-button>
          <el-button
            v-if="!scope.row.enableEdit"
            size="mini"
            @click="handleEdit(scope.row)"
          >编辑
          </el-button>
          <el-button
            v-else
            size="mini"
            @click="beforeClose(scope.row)"
          >取消
          </el-button>
          <el-popconfirm
            v-if="!scope.row.enableEdit"
            title="是否要删除该用户？"
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
        </el-form-item><el-form-item label="邮箱">
          <el-input v-model="temp.email" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="beforeClose">取 消</el-button>
        <el-button type="primary" @click="commitAddData">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getList, updateUser, createUser, deleteUser } from '@/api/systemManage/users'
import { parseTime } from '@/utils'
export default {
  name: 'TemplateTypes',
  data() {
    return {
      query: { // 查询的过滤条件
        name: ''
      },
      loading: true,
      list: [],
      activeItem: {},
      flags: {
        addDialogVisible: false
      },
      temp: {
        'id': 1,
        'username': '',
        'password': ''
      }
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    parseTime(time, format) {
      return parseTime(time, format)
    },
    handleEdit(row) {
      row.enableEdit = !row.enableEdit
      this.temp = row
      this.temp.password = ''
    },
    beforeClose(row) {
      row.enableEdit = !row.enableEdit
      this.flags.addDialogVisible = false
      this.temp = {}
    },
    handleAdd() {
      this.flags.addDialogVisible = true
    },
    commitAddData() {
      createUser(this.temp).then(res => {
        this.$message({ type: 'success', message: '添加成功，' })
        this.flags.addDialogVisible = false
        this.temp = {}
        this.getList()
      }).catch(error => {
        console.log(error)
        this.$message({ type: 'error', message: '添加失败！' })
      })
    },
    handleCloseAddDialog() {

    },
    handleSave() {
      const data = Object.assign({}, this.temp)
      if (data.password === '') {
        // console.log(66)
        delete data.password
      }
      // console.log(data)
      updateUser(data).then(res => {
        this.$message({ type: 'success', message: '保存成功，' })
        this.flags.addDialogVisible = false
        this.temp = {}
        this.getList()
      }).catch(error => {
        console.log(error.response)
        this.$message({ type: 'error', message: '必须输入密码.' })
      })
    },
    handleDelete(id) {
      deleteUser(id).then(res => {
        this.$message({ type: 'success', message: '删除成功！' })
        this.getList()
      }).catch(erro => {
        this.$message({ type: 'error', message: '删除失败！' })
      })
    },
    getList() {
      this.loading = true
      getList().then(res => {
        // enableEdit~
        // console.log(res)
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
