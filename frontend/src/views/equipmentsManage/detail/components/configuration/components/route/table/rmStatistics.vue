<template>
  <div class="content">
    <div ref="chart" class="chart" />
  </div>
</template>

<script>
import { isArray } from '@/utils/validate'
export default {
  name: 'RmStatistics',
  props: {
    rmStatistics: {
      type: Array
    }
  },
  computed: {
    ip() {
      return this.$route.params.ip
    }
  },
  mounted() {
    this.loadingInit = false
    this.$nextTick(() => {
      this.initChart()
    })
  },
  methods: {
    initChart() {
      // console.log(this.rmStatistics)
      // source: [
      //       ['product', '2015', '2016', '2017'],
      //       ['Matcha Latte', 43.3, 85.8, 93.7],
      //       ['Milk Tea', 83.1, 73.4, 55.1],
      //       ['Cheese Cocoa', 86.4, 65.2, 82.5],
      //       ['Walnut Brownie', 72.4, 53.9, 39.1]
      //   ]
      const source = [['protocolId', '总数', '激活']]
      if (isArray(this.rmStatistics)) {
        this.rmStatistics.forEach(item => {
          const temp = [item.protocolId, item.totalNum, item.activeNum]
          source.push(temp)
        })
      }
      this.chart = this.$echarts.init(this.$refs.chart, 'walden')

      this.chart.setOption({
        title: {
          text: '路由统计信息',
          subtext: this.ip,
          left: 'center'
        },
        legend: {
          right: 10
        },
        tooltip: {},
        dataset: {
          source: source
        },
        xAxis: { type: 'category' },
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
          { type: 'bar', label: {
            show: true,
            position: 'top'
          }},
          { type: 'bar', label: {
            show: true,
            position: 'top'
          }}
        ]
      })
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
</style>
