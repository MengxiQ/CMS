<template>
  <div class="content">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="Send" name="1">
        <template slot="title"><i class="el-icon-s-promotion title">Request</i></template>
        <el-row class="request-content">
          <el-col :span="17" class="left">
            <codemirror v-model="temp.sendCodeData" :options="sendCmOptions" />
          </el-col>
          <el-col :span="7" class="right">
            <i class="el-icon-refresh refresh" title="重置" @click="handleReset" />
            <el-divider content-position="left">NETCONF用户</el-divider>
            <el-form size="mini" label-position="middle" label-width="60px">
              <el-form-item label="IP地址">
                <el-input v-model="temp.ip" placeholder="设备IP地址" />
              </el-form-item>
              <el-form-item label="用户名">
                <el-input v-model="temp.user.username" placeholder="NetConf用户名" />
              </el-form-item>
              <el-form-item label="密码">
                <el-input v-model="temp.user.password" placeholder="NetConf用户密码" type="" />
              </el-form-item>
              <el-form-item label="端口号">
                <el-input v-model="temp.user.port" placeholder="端口号" />
              </el-form-item>
              <el-form-item label="厂商" placeholder="厂商标识符">
                <el-select v-model="temp.device_params">
                  <el-option label="华为" value="huawei" />
<!--                  <el-option label="锐捷" :value="'ruijie'" />-->
<!--                  <el-option label="思科" :value="'cisco'" />-->
                </el-select>
              </el-form-item>
<!--              <el-form-item label="HostKey">-->
<!--                <el-input-->
<!--                  v-model="temp.user.hostkey"-->
<!--                  placeholder="请输入HostKey"-->
<!--                  type="textarea"-->
<!--                  :autosize="{ minRows: 1, }"-->
<!--                />-->
<!--              </el-form-item>-->
            </el-form>
            <el-divider content-position="left">配置选项</el-divider>
            <el-form size="mini" label-width="60px">
              <el-form-item label="配置库">
                <el-select v-model="temp.action.source" size="mini" :disabled="temp.action.name === 'get'">
                  <el-option label="running" value="running">running</el-option>
                  <el-option label="candidate" value="candidate">candidate</el-option>
                  <el-option label="startup" value="startup">startup</el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="动作">
                <el-radio-group v-model="temp.action.name" style="" size="mini">
                  <el-radio-button label="get" border>get</el-radio-button>
                  <el-radio-button label="get-config" border>get-config</el-radio-button>
                  <el-radio-button label="edit-config" border>edit-config</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item>
                <el-button :disabled="isLoading" style="float: right" size="mini" type="primary" :icon="isLoading ? 'el-icon-loading' : 'el-icon-s-promotion'" @click="handleSend">发送</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
      </el-collapse-item>
      <el-collapse-item title="response" name="2">
        <template slot="title"><i class="el-icon-video-camera-solid title">Response</i></template>
        <div class="response-content">
          <codemirror class="code" v-model="resCodeData" :options="resCmOptions" />
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
// import 'codemirror/mode/javascript/javascript.js' // 必须提前引入，因为vue 貌似没有无法在实例初始化后再动态加载对应 J
import 'codemirror/mode/xml/xml' // 必须提前引入，因为vue 貌似没有无法在实例初始化后再动态加载对应
import 'codemirror/theme/cobalt.css'
import { sendXmlConfig } from '@/api/configManage/tools'
// import theme style
// import 'codemirror/theme/base16-dark.css'
export default {
  data() {
    return {
      isLoading: false,
      activeNames: ['1', '2'],
      resCodeData: '<!-- 返回的信息... -->\n',
      sendCmOptions: {
        // tabSize: 4,
        mode: 'text/xml',
        tabSize: 4,
        // mode: 'text/javascript',
        // theme: 'base16-dark',
        theme: 'cobalt',
        lineNumbers: true,
        line: true,
        readOnly: false
      },
      resCmOptions: {
        tabSize: 4,
        mode: 'text/xml',
        theme: 'cobalt',
        lineNumbers: false,
        line: true,
        readOnly: true
      },
      temp: {
        'ip': '192.168.100.102',
        'user': {
          'username': 'client001',
          'password': 'Admin@wlx@2017',
          'port': 22,
          'device_params': 'huawei',
          'hostkey': null
        },
        'action': {
          'source': 'running',
          'name': 'get-config'
        },
        'sendCodeData': '<!-- 编辑模板... -->\n'
      }
    }
  },
  methods: {
    handleSend() {
      this.isLoading = true
      const notify = this.$notify({
        title: '下发配置',
        message: '<i class="el-icon-loading"></i>正在向[' + this.temp.ip + ']下发配置.',
        duration: 0,
        dangerouslyUseHTMLString: true,
        showClose: false
      })
      sendXmlConfig(this.temp).then(res => {
        this.resCodeData = res.data
        this.$message({ type: 'success', message: '下发成功.' })
        notify.close()
        this.isLoading = false
      }).catch(error => {
        console.log(error.response)
        this.$message({ type: 'error', message: String(error.response['data']['msg']) })
        notify.close()
        this.isLoading = false
      })
    },
    handleChange(val) {
    },
    handleReset() {
      this.temp = {
        'ip': '',
        'equipment': '',
        'username': '',
        'password': '',
        'port': 22,
        'device_params': 'huawei',
        'hostkey': null,
        'source': 'running',
        'action': 'get-config'
      }
    }
  }
}
</script>

<style lang="less" scoped>
@border-color: #c4c4c4;
.request-content {
  //background: rgb(247,247,247);
  border: @border-color solid 1px;
}
.left {
  //padding-top: 20px;
  //padding-right: 20px;
}

.right {
  //background: #f9f9f9;
  height: auto;
  padding: 0 10px;
  position: relative;
  border-left: solid 1px @border-color;
}

.refresh {
  color: coral;
  position: absolute;
  top: 4px;
  left: 4px;
  font-weight: bolder;
}

.refresh:hover {
  cursor: pointer;
}

.content {
  padding: 10px;
}

.title {
  font-size: larger;
}
.response-content {
  background: #e6e8ea;
  border: @border-color solid 1px;
}
</style>
