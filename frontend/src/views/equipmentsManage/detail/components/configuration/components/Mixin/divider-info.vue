<template>
  <el-divider content-position="left">
    <span style="font-size: smaller">数据源：{{ dataSource }}</span>
  </el-divider>
</template>

<script>
export default {
  name: 'DividerInfo',
  props: {
    dataSource: {
      type: String
    }
  }
}
</script>

<style scoped>

</style>
