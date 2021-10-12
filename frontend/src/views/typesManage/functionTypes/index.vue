<template>
  <div class="content">
    <button-group @add="handleAdd" @refresh="getList"></button-group>
    <el-table :data="list">
      <el-table-column type="index" width="50" />
      <el-table-column label="类型名称" prop="name">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.name }}</span>
          <el-input v-else v-model="scope.row.name" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="类型描述" prop="remark">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.remark }}</span>
          <el-input v-else v-model="scope.row.remark" type="textarea" size="mini" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template slot-scope="scope">
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
            title="这是一段内容确定删除吗？"
            @onConfirm="handleDelete(scope.row.id)"
          >
            <el-button
              slot="reference"
              size="mini"
              type="danger"
            >删除
            </el-button>
          </el-popconfirm>

        </template>
      </el-table-column>
    </el-table>
    <!--    添加弹出框-->
    <el-dialog
      title="添加功能类型"
      :visible.sync="flags.addDialogVisible"
      width="50%"
      :before-close="beforeClose"
    >
      <el-form>
        <el-form-item label="类型名称">
          <el-input v-model="typeTemp.name" />
        </el-form-item>
        <el-form-item label="类型描述">
          <el-input v-model="typeTemp.remark" />
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
import { addFunction, updateFunction, deleteFunction } from '@/api/typesManage'
import { typeMixin } from '@/views/typesManage/mixin/typeMixin'
import ButtonGroup from '@/views/typesManage/componments/buttonGroup'

export default {
  name: 'FunctionTypes',
  components: { ButtonGroup },
  mixins: [typeMixin],
  data() {
    return {
      list: [],
      temp: {},
      flags: {
        addDialogVisible: false
      },
      typeTemp: {
        name: '',
        remark: ''
      }
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    beforeClose() {
      this.flags.addDialogVisible = false
      this.typeTemp = {
        name: '',
        remark: ''
      }
    },
    handleAdd() {
      this.flags.addDialogVisible = true
    },
    commitAddData() {
      addFunction(this.typeTemp).then(res => {
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
      updateFunction(row).then(res => {
        this.$message({ type: 'success', message: '保存成功，' })
        this.beforeClose()
        this.getList()
      }).catch(error => {
        console.log(error)
        this.$message({ type: 'error', message: '保存失败！' })
        this.getList()
      })
    },
    handleDelete(id) {
      deleteFunction(id).then(res => {
        this.$message({ type: 'success', message: '删除成功！' })
        this.getList()
      }).catch(erro => {
        this.$message({ type: 'error', message: '删除失败！' })
      })
    },
    getList() {
      this.updateType('functionTypes')
      // this.list = this.$store.getters.functionTypes
      // getFunctionsList().then(res => {
      //   // enableEdit
      //   const data = res.map(item => {
      //     item.enableEdit = false
      //     return item
      //   })
      //   this.list = data
      // }).catch(erro => {
      //   console.log(erro)
      //   this.$message({ type: 'error', message: '获取列表失败！' })
      // })
    }
  }
}
</script>

<style scoped>

  .content {
    padding: 20px;
  }
</style>
