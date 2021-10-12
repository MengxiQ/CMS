<template>
  <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow" width="50%">
    <el-form ref="dataForm" :model="temp" label-position="left" label-width="80px" style="width:100% ;height: 100%">
      <div class="dialog_body">
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

        <el-form-item label="创建时间" prop="stock_date" disabled>
          <el-date-picker v-model="temp.stock_date" type="datetime" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="temp.remark" type="textarea" />
        </el-form-item>
      </div>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogEditShow = false">
        取消
      </el-button>
      <el-button type="primary" @click="dialogEditStatus==='create'?createData():updateData()">
        确认
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'EditDialog'
}
</script>

<style scoped>

</style>
