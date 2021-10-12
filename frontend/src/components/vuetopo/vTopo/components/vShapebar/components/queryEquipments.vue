<template>
  <div>
<!--    <h4 style="font-weight: bold;padding: 0 0 10px 0;">添加设备</h4>-->
    <el-form size="mini" :inline="true">
      <el-form-item label="起始IP:">
        <el-input v-model="seachData.beginIP" placeholder="起始IP"/>
      </el-form-item>
      <el-form-item label="结束IP:">
        <el-input v-model="seachData.endIP" placeholder="结束IP"/>
      </el-form-item>
      <el-form-item>
        <el-button icon="el-icon-search" type="primary" @click="getList">查询</el-button>
      </el-form-item>
      <ul class="select-equipment-contair-show">
        <el-table
          ref="multipleTable"
          :data="list"
          tooltip-effect="dark"
          style="width: 100%"
          height="300"
          @selection-change="handleSelectionChange"
        >
          <el-table-column
            type="selection"
            width="55"
          />
          <el-table-column
            label="IP"

            prop="ip"
          />
          <el-table-column
            prop="name"
            label="名称"
          />
          <el-table-column
            prop="type.name"
            label="类型"
          />
          <el-table-column
            prop="unittype.name"
            label="型号"
          />
        </el-table>
      </ul>
    </el-form>
    <br>
    <el-button style="float: right;margin-right: 10px" type="primary" size="mini" @click="onAdd">添加</el-button>
  </div>
</template>

<script>
import { fetchEquipmentListByIp } from '@/api/equipment'

export default {
  name: 'QueryEquipment',
  data() {
    return {
      seachData: {
        beginIP: '',
        endIP: ''
      },
      list: [],
      multipleSelection: []
    }
  },
  methods: {
    getList() {
      fetchEquipmentListByIp(this.seachData).then(res => {
        this.list = res
      }).catch()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    onAdd() {
      this.$emit('selected', this.multipleSelection)
    }
  }
}
</script>

<style scoped>

</style>
