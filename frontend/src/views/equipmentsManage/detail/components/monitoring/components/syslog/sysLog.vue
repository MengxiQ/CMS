<template>
  <div>
    <el-divider content-position="left">设备日志<el-link type="primary" style="margin-left:5px;font-size: smaller" @click="getList">刷新</el-link></el-divider>
    <div v-loading="loadingInit" style="padding: 10px; margin-left: 30px">
      <span style="font-size: smaller">排序：</span>
    <el-radio-group v-model="reverse">
      <el-radio :label="false">正序</el-radio>
      <el-radio :label="true">倒序</el-radio>
    </el-radio-group>
    </div>
    <el-timeline :reverse="reverse">
      <el-timeline-item v-for="(item, key) in list" :key="key" :timestamp="parseTime(new Date(Date.parse(item.logContent.match('^.{20}')[0])))" placement="top">
        <el-card>
<!--          <h4>{{item.sequence}}</h4>-->
          <p style="color: #1f2f3d; ">{{item.logContent}}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline></div>
</template>

<script>
import { getSysLog } from '@/api/detail/monitoring/monitoring'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { isArray } from '@/utils/validate'
import { parseTime } from '@/utils'
export default {
  name: 'SysLog',
  mixins: [baseMinxin],
  data() {
    return {
      reverse: false
    }
  },
  methods: {
    parseTime(time) {
      return parseTime(time)
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getSysLog(query).then(res => {
        const result = res.data.syslog.icLogBuffers.icLogBuffer
        this.list = isArray(result) ? result : Array(result)
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>

</style>
