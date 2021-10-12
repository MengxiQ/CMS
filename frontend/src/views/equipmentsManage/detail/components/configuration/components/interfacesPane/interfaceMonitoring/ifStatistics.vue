<template>
  <div class="content">
    <div ref="chart" class="chart" />
  </div>
</template>

<script>
export default {
  name: 'IfStatistics',
  props: {
    ifStatistics: {
      type: Object
    },
    ifName: {
      type: String
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
      // str.match('rcv(?<p>.*)') groups.p

      // 过滤出 receives 和 sends
      const receives = []
      const sends = []

      for (const key in this.ifStatistics) {
        const receive = key.match('^rcv(?<p>.*)') || key.match('^receive(?<p>.*)')
        const send = key.match('^send(?<p>.*)')
        if (receive) {
          const item = {}
          item[receive.groups.p] = this.ifStatistics[key]
          receives.push(item)
        }
        if (send) {
          const item = {}
          item[send.groups.p] = this.ifStatistics[key]
          sends.push(item)
        }
      }
      // console.log(receives, sends)
      const source = [['名称', '接收', '发送']]
      receives.forEach(item => {
        let key1 = null
        let key2 = null
        for (const k1 in item) {
          key1 = k1
        }
        sends.forEach(s => {
          for (const k2 in s) {
            key2 = k2
          }
          if (key1 === key2) {
            // console.log(key1)
            let name = key1
            switch (key1) {
              case 'Byte' : { name = '字节总数'; break }
              case 'Packet' : { name = '报文总数'; break }
              case 'UniPacket' : { name = '单播总数'; break }
              case 'MutiPacket' : { name = '组播总数'; break }
              case 'BroadPacket' : { name = '广播总数'; break }
              case 'ErrorPacket' : { name = '错误总数'; break }
              case 'DropPacket' : { name = '丢弃总数'; break }
            }
            source.push([name, item[key1], s[key1]])
          }
        })
      })
      // console.log(source)
      this.chart = this.$echarts.init(this.$refs.chart, 'walden')

      this.chart.setOption({
        legend: {
          right: 100,
          top: 4
        },
        title: {
          text: '接口Mib统计信息',
          left: 'center',
          subtext: this.ip + '-' + this.ifName
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
        toolbox: {
          feature: {
            // dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar'] },
            // restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        dataset: {
          source: source
        },
        xAxis: {
          type: 'category',
          axisPointer: {
            type: 'shadow'
          },
          axisLabel: {
            interval: 0
          }
        },
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
    /*background-color: red;*/
  }
  .chart {
    width: 100%;
    min-height: 500px;
    /*background: red;*/
  }
</style>
