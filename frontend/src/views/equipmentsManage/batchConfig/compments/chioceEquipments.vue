<template>
  <div class="content">
    <el-row>
      <el-col :span="20" :offset="2">
        <el-form size="mini" :inline="true">
          <el-form-item label="起始IP:">
            <el-input v-model="query.beginIP" placeholder="起始IP"/>
          </el-form-item>
          <el-form-item label="结束IP:">
            <el-input v-model="query.endIP" placeholder="结束IP"/>
          </el-form-item>
          <el-form-item label="厂商">
            <el-select clearable v-model="query.vendor" placeholder="厂商">
              <el-option label="华为" value="huawei"></el-option>
              <el-option label="锐捷" value="ruijie"></el-option>
              <el-option label="思科" value="cisco'"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-search" type="primary" @click="queryEquipments">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="20" :offset="2">
        <el-table
          ref="multipleTable"
          :data="list"
          tooltip-effect="dark"
          style="width: 100%"
          height="200"
          @selection-change="SelectionEquipemntChange"
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
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { fetchEquipmentListByIp } from '@/api/equipment'

export default {
  name: 'ChioceEquipments',
  data() {
    return {
      query: {
        beginIP: '',
        endIP: '',
        vendor: ''
      },
      list: [],
      selectedEquipments: []
    }
  },
  methods: {
    queryEquipments() {
      fetchEquipmentListByIp(this.query).then(res => {
        this.list = res
      }).catch()
    },
    SelectionEquipemntChange(val) {
      this.selectedEquipments = val
      this.$emit('selectedequipments', this.selectedEquipments)
    }
  }
}
</script>

<style scoped>
.content {
  margin-top: 35px;
}
</style>
