<template>
  <div class="content">
    <button-group @add="handleAdd" @refresh="getList"></button-group>
    <el-table v-loading="loading" :data="list">
      <el-table-column type="index" width="50"></el-table-column>
      <el-table-column label="类型名称" prop="name">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.name }}</span>
          <el-input v-else v-model="scope.row.name" size="mini"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="类型描述" prop="remark">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.remark }}</span>
          <el-input v-else v-model="scope.row.remark" type="textarea" size="mini"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="厂商" prop="vendor">
        <template slot-scope="scope">
          <span v-if="!scope.row.enableEdit">{{ scope.row.vendor }}</span>
          <el-select v-else v-model="scope.row.vendor" size="mini" >
            <el-option
              v-for="(item, key) in $store.getters.vendorTypes"
              :key="key"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="handleSave(scope.row)" v-if="scope.row.enableEdit">保存
          </el-button>
          <el-button
            v-if="!scope.row.enableEdit"
            size="mini"
            style="margin-right: 5px"
            @click="scope.row.enableEdit = !scope.row.enableEdit">编辑
          </el-button>
          <el-button
            v-else
            size="mini"
            @click="scope.row.enableEdit = !scope.row.enableEdit">取消
          </el-button>
          <el-popconfirm
            title="这是一段内容确定删除吗？"
            @onConfirm="handleDelete(scope.row.id)"
          >
            <el-button
              size="mini"
              type="danger"
              slot="reference"
            >删除
            </el-button>
          </el-popconfirm>

        </template>
      </el-table-column>
    </el-table>
    <!--    添加弹出框-->
    <el-dialog
      title="添加设备型号"
      :visible.sync="flags.addDialogVisible"
      width="50%"
      :before-close="beforeClose">
      <el-form>
        <el-form-item label="类型名称">
          <el-input v-model="typeTemp.name"></el-input>
        </el-form-item>
        <el-form-item label="类型描述">
          <el-input v-model="typeTemp.remark"></el-input>
        </el-form-item>
        <el-form-item label="厂商">
          <el-select v-model="typeTemp.vendor" clearable>
            <el-option
              v-for="(item, key) in this.$store.getters.vendorTypes"
              :key="key"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
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
import { addUnitType, deleteUnitType, updateUnitType } from '@/api/typesManage'
import { typeMixin } from '@/views/typesManage/mixin/typeMixin';
import ButtonGroup from '@/views/typesManage/componments/buttonGroup'

export default {
  name: 'UnitTypes',
  components: { ButtonGroup },
  mixins: [typeMixin],
  data() {
    return {
      typeTemp: {
        name: '',
        remark: '',
        vendor: ''
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
      this.loading = true
      addUnitType(this.typeTemp).then(res => {
        this.loading = false
        this.$message({ type: 'success', message: '添加成功，' })
        this.beforeClose()
        this.getList()
      }).catch(error => {
        this.loading = false
        console.log(error)
        this.$message({ type: 'error', message: '添加失败！' })
      })
    },
    handleCloseAddDialog() {

    },
    handleSave(row) {
      this.loading = true
      updateUnitType(row).then(res => {
        this.$message({ type: 'success', message: '保存成功，' })
        this.beforeClose()
        this.getList()
      }).catch(error => {
        console.log(error)
        this.loading = false
        this.$message({ type: 'error', message: '保存失败！' })
        this.getList()
      })
    },
    handleDelete(id) {
      this.loading = true
      deleteUnitType(id).then(res => {
        this.loading = false
        this.$message({ type: 'success', message: '删除成功！' })
        this.getList()
      }).catch(erro => {
        this.loading = false
        this.$message({ type: 'error', message: '删除失败！' })
      })
    },
    getList() {
      this.loading = true
      this.updateType('unitTypes')
      // getUnitTypesList().then(res => {
      //   // enableEdit
      //   this.list = res.map(item => {
      //     item.enableEdit = false
      //     return item
      //   })
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
