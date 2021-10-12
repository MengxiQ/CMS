<template>
  <div class="page-content content">
    <!--    # 设置配置库-->
    <!--    # 更改放到store中-->
    <el-divider content-position="left"><i class="el-icon-s-tools" style="margin-right: 5px" />配置选项</el-divider>
    <el-form size="mini" label-position="right" label-width="100px">
      <el-form-item label="配置数据库:">
        <el-select v-model="source">
          <el-option label="running" value="running" />
          <el-option label="candidate" value="candidate" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <!--          <el-button size="mini" type="" @click="source = this.$store.getters.source">取消</el-button>-->
        <el-button size="mini" type="primary" @click="save">设置</el-button>
      </el-form-item>
    </el-form>
    <div v-if="this.$store.getters.source === 'candidate'">
      <el-divider content-position="left"><i class="el-icon-s-tools" style="margin-right: 5px" />candidate管理</el-divider>
      <el-radio-group v-model="configMode" size="mini" style="margin: 10px">
        <el-radio-button label="Schema" value="Schema"></el-radio-button>
        <el-radio-button label="Yang" value="Yang"></el-radio-button>
      </el-radio-group>
      <el-form size="mini" label-position="right" label-width="100px">
        <el-form-item label="Candidate：">
          <el-button size="mini" type="primary" @click="createCandidate">创建</el-button>
        </el-form-item>
        <el-form-item label="试运行：">
          <el-switch
            v-model="temp.attempt"
            active-color="#13ce66"
          />
          <el-form size="mini" :disabled="!temp.attempt">
            <el-form-item label="">
              超时时间：<el-input v-model="temp.timeout" placeholder="默认值：600秒" style="width: 120px" />
              <span style="margin-left: 5px; margin-right: 50px">(60 to 65535)s</span>
              <label v-if="configMode !== 'Schema'" style="font-weight: normal">令牌：<el-input v-model="temp.persist " placeholder="可选, 请牢记" style="width: 200px" /></label>
            </el-form-item>
          </el-form>
        </el-form-item>
        <el-form-item label="提交：">
          <label v-if="configMode !== 'Schema'" style="font-weight: normal">令牌：<el-input v-model="temp.persist_id" placeholder="可选，已存在的试运行令牌" style="width: 200px;margin-right: 50px;" :disabled="temp.attempt" /></label>
          <el-popconfirm
            title="是否提交选项和配置？"
            @onConfirm="commitConfig"
          >
            <el-button slot="reference" size="mini" type="primary">commit</el-button>
          </el-popconfirm>
        </el-form-item>
        <el-form-item>
          <el-divider content-position="left">试运行队列</el-divider>
          <ul class="log">
            <li v-for="(item, key) in queues" :key="key" class="log-item" :class="{'log-item-timeout': !item.flag}">
              <span class="log-item-param"><i class="el-icon-s-flag" style="margin-right: 5px" />{{ key }}</span>
              <span v-if="configMode !== 'Schema'" class="log-item-param">令牌：{{ item.persist }}</span>
              <span class="log-item-param"><i class="el-icon-timer" />秒表：{{ item.timer }}s</span>
              <i v-if="item.flag" class="el-icon-loading"></i>
            </li>
          </ul>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { commit } from '@/api/detail/manage/commit'
import { createVlans } from '@/api/detail/vlans'
export default {
  data() {
    return {
      configMode: 'Schema',
      source: this.$store.getters.source,
      loading: false,
      temp: {
        attempt: false,
        timeout: null,
        persist: null,
        persist_id: null
      },
      queues: []
    }
  },
  computed: {
    ip() {
      return this.$route.params.ip
    }
  },
  methods: {
    save() {
      this.$store.commit('settingSource', this.source)
      this.$message({ type: 'success', message: '设置成功。' })
    },
    commitConfig() {
      this.loading = true
      commit(this.ip, this.temp).then(res => {
        this.$message({ type: 'success', message: '提交成功。' })
        // 提交成功再创建候选库
        this.loading = false
        if (this.temp.attempt) {
          // 记录运行队列
          const queue = { persist: this.temp.persist, timer: this.temp.timeout, flag: true }
          this.clearAlltimer()
          this.queues.push(queue)
          this.createtimer(queue)
        } else {
          // 如果直接提交，则会清除所有的队列
          this.clearAlltimer()
        }
      }).catch(error => {
        const data = error.response['data']
        this.$message({ type: 'warning', message: '提交失败.(' + data['msg'] + ')' })
        this.loadingInit = false
      })
    },
    clearAlltimer() {
      this.queues.forEach(item => {
        item.flag = false
        item.timer = 0
      })
    },
    createtimer(queue) {
      const timer = setInterval(_ => {
        if (queue.timer <= 0) {
          clearInterval(timer)
          queue.flag = false
        } else {
          queue.timer -= 1
        }
      }, 1000)
    },
    createCandidate() {
      /** 创建一个vlan1，以便创建候选库 **/
      const data = {
        ip: this.ip,
        data: { 'vlanId': '1' },
        source: this.$store.getters.source
      }
      this.loadingInit = true
      createVlans(data).then(res => {
        this.$message({ type: 'success', message: '创建新的candidate数据库' })
        this.temp = {}
      }).catch(error => {
        const data = error.response['data']
        this.$message({ type: 'error', message: '创建新的candidate数据库失败.(' + data['msg'] + ')' })
        this.loadingInit = false
      })
    }

  }
}
</script>

<style scoped>
  ul,li{
    list-style: none;
    /*padding: 0;*/
    /*margin: 0;*/
  }
  .content {
  }
  .log {
    /*background-color: green;*/
    min-height: 200px;
    padding: 10px 0;
  }
  .log-item {
    padding: 5px 0;
    width: 400px;
    background-color: rgb(19,206,102);
    margin-bottom: 1px;
  }
  .log-item-timeout {
    background-color: orange;
  }
  .log-item:hover {
    cursor: pointer;
    background-color: #66b1ff;
  }
  .log-item-param {
    padding: 10px 20px;
  }
</style>
