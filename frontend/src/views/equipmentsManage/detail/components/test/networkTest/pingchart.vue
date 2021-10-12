<template>
  <div>
    <el-page-header @back="goBack" >
      <template slot="content">
        <a class="el-icon-refresh refresh" title="刷新" @click="refresh"></a>
      </template>
    </el-page-header>
    <!--    <div><span>Ping-{{ activeData.pingResultDetails.pingResultDetail[0].ipAddr }}</span></div>-->
    <div v-loading="loadingInit" class="content">
      <div ref="chart" class="chart" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pingchart',
  props: {
    activeData: {
      type: Object
    }
  },
  data() {
    return {
      loadingInit: false
    }
  },
  mounted() {
    this.loadingInit = true
    this.$nextTick(() => {
      this.initChart()
    })
  },
  methods: {
    goBack() {
      this.$emit('back')
    },
    refresh() {
      this.$emit('refresh')
    },
    initChart() {
      const s_data = this.activeData.pingResultDetails.pingResultDetail // []

      const xAxisData = []
      const seriesData = []
      s_data.forEach(item => {
        xAxisData.push(item.index)
        seriesData.push(item.rtt)
      })
      this.chart = this.$echarts.init(this.$refs.chart, 'walden')
      this.chart.setOption({
        title: {
          text: this.activeData.testName,
          subtext: 'ping' + this.activeData.pingResultDetails.pingResultDetail[0].ipAddr,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        legend: {
          data: ['延迟'],
          right: 20,
          top: 10
        },
        xAxis: {
          name: 'packet',
          type: 'category',
          data: xAxisData
        },
        yAxis: {
          name: '延迟',
          type: 'value',
          axisLabel: {
            formatter: '{value} ms'
          }
        },
        series: [{
          name: '延迟',
          data: seriesData,
          type: 'line'
        }]
      })

      this.loadingInit = false
    }
  }
}
</script>

<style scoped>
  .content {
    background-color: white;
  }
  .chart {
    width: 100%;
    min-height: 400px;
    /*background: red;*/
  }
  .refresh {
    color: #20a0ff;
  }
  .refresh:hover {
    cursor: pointer;
  }
</style>
