<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎, {{ name }}。</div>
    <effects></effects>
    <panel-group />
    <!--    <li>折线图：每日配置成功和失败的数量</li>-->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PanelGroup from '@/views/home/compements/PanelGroup'
import Effects from '@/views/home/compements/effects'

export default {
  name: 'Dashboard',
  components: { Effects, PanelGroup },
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 20px;
    line-height: 46px;
  }
}
</style>
