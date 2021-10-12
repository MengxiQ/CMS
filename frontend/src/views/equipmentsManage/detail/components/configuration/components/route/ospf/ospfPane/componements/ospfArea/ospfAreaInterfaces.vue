<template>
  <div>
    <el-divider content-position="left">接口列表</el-divider>
    <el-table
      :data="list"
    >
      <el-table-column label="ifName" prop="ifName" />
      <el-table-column label="networkType" prop="networkType" />
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'OspfAreaInterfaces',
  props: {
    list: {
      type: Array,
      default() {
        return []
      }
    }
  }
}
</script>

<style scoped>

</style>
