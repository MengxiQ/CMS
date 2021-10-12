<template>
  <div class="content">
    <!--    <el-divider content-position="left">测试工具</el-divider>-->
    <!--    <el-tabs active-name="ping">-->
    <!--      <el-tab-pane label="ping测试" name="ping" lazy><ping-test/></el-tab-pane>-->
    <!--      <el-tab-pane label="tracert测试" name="tracert" lazy>tracert</el-tab-pane>-->
    <!--    </el-tabs>-->
    <ping-test />
  </div>
</template>

<script>
import PingTest from '@/views/equipmentsManage/detail/components/test/networkTest/pingTest'
export default {
  components: { PingTest }
}
</script>

<style scoped>

</style>
