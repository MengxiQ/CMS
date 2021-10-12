<template>
  <div class="basePane">
    <monitoring :ip="ip"></monitoring>
  </div>
</template>

<script>
import Monitoring from '@/views/equipmentsManage/detail/components/monitoring/components/basePane/monitoring/monitoring'

export default {
  name: 'BasePane',
  components: { Monitoring },
  props: {
  },
  computed: {
    ip() {
      return this.$route.params.ip
    }
  },
  data() {
    return {
    }
  },
  created() {

  },
  methods: {}
}
</script>

<style scoped>
  .basePane{
    /*background: rgb(246, 248, 252);*/
    /*padding: 10px;*/
    /*padding-bottom: 100px;*/
  }
</style>
