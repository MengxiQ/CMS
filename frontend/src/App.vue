<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
// echart 主题
import '@/views/equipmentsManage/detail/components/configuration/components/route/table/echat-theme.js'
export default {
  name: 'App',
  created() {
    this.$store.dispatch('getTypes')
  }
}
</script>
<style>
  .CodeMirror{
    height: 500px !important;
  }
  /*设置el-tabs border-card类型下的 标签栏为白色 */
  .el-tabs--border-card>.el-tabs__header{
  background: white !important;
}
</style>
