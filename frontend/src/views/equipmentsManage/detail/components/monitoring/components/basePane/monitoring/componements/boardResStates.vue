<template>
  <div>
    <pane
      :title="'单板：'+data.board.boardName + '        槽位：' + data.board.boardPosition['#text'] + '   实体索引：'+ data.board.entIndex"
      @reload="$emit('reload')">
      <div v-loading="loading" style="min-height: 100px">
        <ul class="content">
          <li v-if="data.mpu">
            <ul class="mpu">
              <li>角色：
                <i v-if="data.mpu.lsRole === 'mmb'" style="color: green" class="el-icon-success">主控板</i>
                <i v-else style="color: goldenrod" class="el-icon-s-flag">主控板</i>
              </li>
              <li>运行时长：{{ formatSeconds(parseInt(data.mpu.upTime)) }}</li>
              <li>硬件类型：{{ data.mpu.boardType }}</li>
              <li>SDRAM空间：{{ data.mpu.sdramSize }}</li>
              <li>NVRAM空间：{{ data.mpu.nvramSize }}</li>
              <li>Flash空间：{{ data.mpu.flashSize }}</li>
            </ul>
          </li>
          <li v-if="data.lpu">
            <ul class="mpu">
              <li>角色：
                <i style="color: green" class="el-icon-success">接口板</i>
              </li>
              <li>运行时长：{{ formatSeconds(parseInt(data.lpu.upTime)) }}</li>
              <li>硬件类型：{{ data.lpu.boardType }}</li>
              <li>SDRAM空间：{{ data.lpu.sdramSize }}</li>
              <li>Flash空间：{{ data.lpu.flashSize }}</li>
              <li>subSlotNum：{{ data.lpu.subSlotNum }}</li>
              <li>picNum：{{ data.lpu.picNum }}</li>
            </ul>
          </li>
          <li class="content-item">
            <span class="name">CPU占用率</span>
            <span class="progress">
              <el-progress :color="customColors" :text-inside="true" :stroke-width="18"
                           :percentage="parseInt(data.board.cpuUsage)"/>
            </span>
          </li>
          <li class="content-item"><span class="name">内存占用率</span>
            <span class="progress">
              <el-progress :color="customColors" :text-inside="true" :stroke-width="18"
                           :percentage="parseInt(data.board.memoryUsage)"/>
            </span>
            <span class="description">
              {{(parseInt(data.board.memTotalSize) / 1024).toFixed(2)}}M可用，
              已用{{ parseInt((data.board.memUsedSize) / 1024).toFixed(2) }}M.</span>
          </li>
        </ul>
      </div>
    </pane>
  </div>
</template>

<script>
import Pane from '@/components/pane/pane'
import { formatSeconds } from '@/utils/time-tool'

export default {
  name: 'BoardResStates',
  components: { Pane },
  props: {
    loading: {
      type: Boolean
    },
    data: {
      type: Object,
      default() {
        return {
          board: { boardPosition: {}}
        }
      }
    }
  },
  data() {
    return {
      customColors: [
        { color: '#f56c6c', percentage: 80 },
        { color: '#e6a23c', percentage: 70 },
        { color: '#1989fa', percentage: 60 },
        { color: '#5cb87a', percentage: 50 }
      ]
    }
  },
  methods: {
    formatSeconds(value) {
      return formatSeconds(value)
    }
  }
}
</script>

<style scoped>
ul, li {
  list-style: none;
  padding: 0;
  margin: 0;
}

.name {
  width: 80px;
}

.progress {
  width: 280px;
}

.content-item {
  margin-bottom: 15px;
}

.mpu {
  margin-bottom: 10px;
}

.mpu > li {
  margin-bottom: 10px;
  display: inline-block;
  width: 50%;
}
</style>
