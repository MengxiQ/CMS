<template>
  <div>
    <div class="content">
      <el-table :data="resultList">
        <el-table-column label="id" prop="id" width="40px"></el-table-column>
        <el-table-column label="设备名称" prop="name"></el-table-column>
        <el-table-column label="ip" prop="ip"></el-table-column>
        <el-table-column label="时间" prop="">
          <template slot-scope="scope">
            <span>{{parseTime(scope.row.time)}}</span>
          </template>
        </el-table-column>
        <el-table-column label="耗时" prop="cost">
          <template slot-scope="props">
            <span>{{props.row.cost}}ms</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" prop="status">
          <template slot-scope="props">
            <div>
            <span :class="{'el-icon-success': props.row.status === 'success','el-icon-error': props.row.status === 'error', 'success': props.row.status === 'success','error': props.row.status === 'error'}">{{props.row.status}}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="描述" prop="des"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { parseTime } from '@/utils'
export default {
  name: 'Result',
  props: {
    resultList: {
      type: Array
    }
  },
  data() {
    return {
    }
  },
  methods: {
    parseTime(time, format) {
      return parseTime(time, format)
    }
  }
}
</script>

<style scoped>
  .content {
    padding: 20px;
  }
  .item {
    list-style: none;
  }
  .param {
    padding: 10px;
  }
  .success {
    color: green;
  }
  .error {
    color: red;
  }
</style>
