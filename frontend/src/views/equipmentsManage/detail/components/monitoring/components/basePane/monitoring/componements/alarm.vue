<template>
  <div>
    <pane :title="'告警统计'" @reload="getList">
      <div v-loading="loadingInit" style="min-height: 100px">
        <div ref="chart" class="chart" />
      </div>
    </pane>
  </div>
</template>

<script>
import Pane from '@/components/pane/pane'
import { monitoringMixin } from '@/views/equipmentsManage/detail/components/monitoring/components/basePane/monitoring/componements/mixins/monitoringMixin'
import { getAlarmList } from '@/api/detail/monitoring/monitoring'

export default {
  name: 'Alarm',
  components: { Pane },
  mixins: [monitoringMixin],
  data() {
    return {
      statistics: []
    }
  },
  mounted() {
  },
  methods: {
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip
      }
      setTimeout(_ => {
        getAlarmList(query).then(res => {
        // console.log(res)
          this.statistics = res.data.fm.alarmStas.alarmSta
          this.statistics = this.statistics.map(item => {
            let name = 'Warning'
            if (item.level === 'Critical') {
              name = '紧急'
            } else if (item.level === 'Major') {
              name = '重要'
            } else if (item.level === 'Minor') {
              name = '次要'
            } else if (item.level === 'Warning') {
              name = '提示'
            }
            return {
              name: name,
              value: item.count
            }
          })
          this.loadingInit = false
          this.$nextTick(() => {
            this.initChart()
          })
        }).catch(error => this.getListError(error))
      }, 2000)
    },
    initChart() {
      this.chart = this.$echarts.init(this.$refs.chart, 'macarons')

      this.chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '1',
          data: ['紧急', '重要', '次要', '提示']
        },
        series: [
          {
            name: '告警统计',
            label: {
              formatter: '{b} : {c}'
            },
            type: 'pie',
            radius: '70%',
            data: this.statistics
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
  .chart {
    width: 100%;
    min-height: 270px;
    /*background: red;*/
  }
</style>
