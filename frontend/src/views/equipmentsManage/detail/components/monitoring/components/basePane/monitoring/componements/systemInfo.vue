<template>
  <div>
    <pane :title="'系统信息'" @reload="getList">
      <div v-loading="loadingInit">
        <ul class="content">
          <li><span class="label">系统名称：</span>
            <span v-if="!isEdit" class="value">{{ list.sysName }}</span>
            <el-input v-else v-model="temp.sysName" style="width: 100px" size="mini" />
            <i title="编辑" style="margin-left: 10px; color: dodgerblue" class="el-icon-edit" @click="handledUpdate" />
            <i v-if="isEdit" title="保存" style="margin-left: 10px; color: dodgerblue" class="el-icon-s-order" @click="handledSave" />
          </li>
          <li><span class="label">产品型号：</span><span class="value">{{ list.productName }}</span></li>
          <li><span class="label">mac地址：</span><span class="value">{{ list.mac }}</span></li>
          <li><span class="label">系统版本：</span><span class="value">{{ list.platformVer }}</span></li>
          <li><span class="label">esn：</span><span class="value">{{ list.esn }}</span></li>
          <li><span class="label">位置：</span><span v-if="!isEdit" class="value">{{ list.sysLocation }}</span><el-input v-else v-model="temp.sysLocation" style="width: 200px" size="mini" /></li>
          <li><span class="label">系统时间：</span><span class="value">{{ timestampToTime(list.sysGmtTime) }}</span></li>
          <li><span class="label">开机时长：</span><span class="value">{{ formatSeconds(list.sysUpTime) }}</span></li>
          <li><span class="label">系统描述：</span><span class="value">{{ list.sysDesc }}</span></li>
        </ul>
      </div>
    </pane>
  </div>
</template>

<script>
import Pane from '@/components/pane/pane'
import { monitoringMixin } from '@/views/equipmentsManage/detail/components/monitoring/components/basePane/monitoring/componements/mixins/monitoringMixin'
import { getSystemInfo, updateSystemInfo } from '@/api/detail/monitoring/monitoring'
import { formatSeconds, timestampToTime } from '@/utils/time-tool'

export default {
  name: 'SystemInfo',
  components: { Pane },
  mixins: [monitoringMixin],
  data() {
    return {
      temp: {
        sysName: '',
        sysLocation: ''
      },
      isEdit: false
    }
  },
  methods: {
    formatSeconds(value) {
      return formatSeconds(value)
    },
    timestampToTime(e) {
      return timestampToTime(e)
    },
    handledUpdate() {
      this.isEdit = !this.isEdit
      this.temp.sysName = this.list.sysName
      this.temp.sysLocation = this.list.sysLocation
    },
    handledSave() {
      const data = {
        ip: this.ip,
        data: this.temp
      }
      updateSystemInfo(data).then(res => {
        this.$message({ type: 'success', message: '更新成功.' })
        this.isEdit = false
        this.getList()
      }).catch(_ => {
        this.$message({ type: 'error', message: '更新失败.' })
      })
    },
    getList() {
      this.loadingInit = true
      setTimeout(_ => {
        getSystemInfo(this.ip).then(res => {
        // console.log(res)
        //   this.list = res.data.system.systemInfo
          this.list = res.data
          this.loadingInit = false
        }).catch(error => this.getListError(error))
      }, 500)
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
  li {
  margin-bottom: 10px;
  display: inline-block;
  width: 100%;
}
</style>
