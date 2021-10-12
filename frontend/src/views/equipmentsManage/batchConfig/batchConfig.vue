<template>
  <div>
    <el-steps style="padding: 15px" :active="active" finish-status="success">
      <el-step title="1:选择模板" description="选择系统的模板或者自定模板。"/>
      <el-step title="2:配置模板" description="给配置模板的参数赋值，点击生成配置后保存进入下一步。" />
      <el-step title="3:选择设备" description="选择需要配置的设备。" />
      <el-step title="4:配置结果" description="批量配置的报告。"/>
    </el-steps>
    <div v-show="active === 0" id="0" class="step-contend">
      <chioce-ttempalte @selectedtemplate="selectedtemplate" @diyconfig="diyconfig" />
    </div>
    <div v-show="active === 1" id="1" class="step-contend">
      <config-template :template="template" :configmode="configMode" @generateconfig="generateconfig" />
    </div>
    <div v-show="active === 2" id="2" class="step-contend">
      <chioce-equipments @selectedequipments="selectedequipments" />
    </div>
    <div v-show="active === 3 || active === 4" id="3" class="step-contend">
      <el-button size="mini" type="" @click="resultList = []">清空</el-button>
      <result :result-list="resultList" />
    </div>
    <div class="button-content">
      <el-button-group>
        <el-button size="mini" type="primary" :disabled="active === 0" @click="previous">上一步</el-button>
        <el-button v-if="active === 2" size="mini" type="success" @click="batchConfig">下发配置</el-button>
        <el-button v-if="active === 0 || active === 1 || active === 3" size="mini" type="primary" :disabled="nextDisable" @click="next">下一步
        </el-button>
        <el-button v-if="active === 4" size="mini" type="success" @click="complete">完成</el-button>
      </el-button-group>
    </div>
  </div>
</template>

<script>
import ChioceTtempalte from '@/views/equipmentsManage/batchConfig/compments/chioceTempalte'
import ChioceEquipments from '@/views/equipmentsManage/batchConfig/compments/chioceEquipments'
import Result from '@/views/equipmentsManage/batchConfig/compments/result'
import ConfigTemplate from '@/views/equipmentsManage/batchConfig/compments/configTemplate'
import { sendXmlConfig } from '@/api/configManage/tools'

export default {
  name: 'BatchConfig',
  components: { ConfigTemplate, Result, ChioceEquipments, ChioceTtempalte },
  data() {
    return {
      active: 0,
      template: {},
      configData: null,
      configMode: '',
      selectedEquipments: [],
      resultList: [],
      notifys: [],
      action: {
        name: 'edit-config',
        TemType: 'merge',
        source: 'running'
      }
    }
  },
  computed: {
    nextDisable() {
      if (this.active === 0 && JSON.stringify(this.template) === '{}') {
        return true
      }
      if (this.active === 1 && this.configData === null) {
        return true
      }
      if (this.active === 2 && JSON.stringify(this.selectedEquipments) === '[]') {
        return true
      }
      if (this.active >= 3) {
        return true
      }
      return false
    }
  },
  methods: {
    previous() {
      if (this.active === 2 && this.configMode === '自定义模板') {
        this.active = 0
      }
      if (this.active > 0) {
        this.active -= 1
      }
    },
    next() {
      if (this.active === 2) {
        this.active = 4
      }
      if (this.active <= 3) {
        this.active += 1
      }
    },
    selectedtemplate(data) {
      // console.log(data)
      this.template = data.selectedtemplate
      this.configMode = data.configMode
    },
    generateconfig(data) {
      if (this.configData !== '') {
        this.configData = data.resCodeData
        this.action = data.action
        this.$message({ type: 'success', message: '保存成功.' })
      } else {
        this.$message({ type: 'error', message: '配置内容不能为空.' })
      }
    },
    diyconfig(data) {
      // console.log(data)
      if (data.resCodeData !== '') {
        this.configData = data.resCodeData
        this.action = data.action
        this.configMode = data.configMode
        this.active = 2
        this.$message({ type: 'success', message: 'diy配置保存成功.' })
      } else {
        this.$message({ type: 'error', message: 'diy配置内容不能为空.' })
      }
    },
    selectedequipments(data) {
      this.selectedEquipments = data
    },
    batchConfig() {
      // 生产promise数组
      const promisArr = this.selectedEquipments.map((item, key) => {
        return new Promise((resolve, reject) => {
          const data = {
            user: item.user,
            ip: item.ip,
            action: this.action,
            // action: {
            //   name: 'edit-config',
            //   source: 'running'
            // },
            sendCodeData: this.configData
          }
          // 下发一个配置
          // 开始日志记录
          const result = {
            id: key + 1,
            name: item.name,
            ip: item.ip,
            time: new Date(),
            cost: '0ms',
            status: 'success',
            des: ''
          }
          const timeBegin = new Date() // 开始记录时间
          // 下发配置
          sendXmlConfig(data).then(res => {
            const timeEnd = new Date()
            const cost = timeEnd - timeBegin // 花费的毫秒数
            result.cost = cost
            this.resultList.push(result)
            resolve('success')
            // this.active = 4
          }).catch(error => {
            const timeEnd = new Date()
            const cost = timeEnd - timeBegin // 花费的毫秒数
            result.cost = cost
            result.status = 'error'
            result.des = error.response.data.msg
            this.resultList.push(result)
            reject('error')
          })
        })
      })
      this.loding = true
      const notify = this.$notify({
        title: '配置',
        message: '<i class="el-icon-loading"></i>正在下发配置...',
        duration: 0,
        dangerouslyUseHTMLString: true
        // showClose: false
      })
      Promise.all(promisArr).then(res => {
        this.$message({ type: 'success', message: '操作完成, 全部配置下发成功.' })
        notify.close()
        this.loding = false
        this.active = 4
      }).catch(error => {
        this.$message({ type: 'warning', message: '操作完成.' })
        notify.close()
        console.log(error)
        this.active = 4
        this.loding = false
      })
    },
    complete() {
      this.template = {}
      this.active = 0
    }
  }
}
</script>

<style scoped>
.button-content {
  position: absolute;
  top: 100px;
  right: 10px;
}
</style>
