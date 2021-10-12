<template>
  <div v-loading="loadingInit" :element-loading-text="'正在连接设备[' + ip + ']'" style="height: 500px; border: 1px solid #eee">
    <el-header>
      <el-menu :default-active="activeIndex" mode="horizontal" @select="handleSelect" style="margin-left: 45px">
        <el-menu-item index="monitoring">
          <i class="el-icon-data-analysis"></i>
          <span slot="title">监控</span></el-menu-item>
        <el-menu-item index="configuration">
          <i class="el-icon-setting"></i>
          <span slot="title">配置</span></el-menu-item>
        <el-menu-item index="test">
          <i class="el-icon-discover"></i>
          <span slot="title">测试</span></el-menu-item>
        <el-menu-item index="maintain">
          <i class="el-icon-suitcase"></i>
          <span slot="title">维护</span></el-menu-item>
        <el-menu-item index="configuration/manage/setting" style="float: right;">
          <span slot="title">
            <span style="font-size: smaller;display: inline-block;height: 40px;width:100px;position: relative">
              <span style="display: block;height: 10px; position: absolute; top: -20px">ip：{{ ip }}</span>
              <span style="display: block; height: 10px; position: absolute">数据库：{{ this.$store.getters.source }}</span>
            </span>
          </span>
        </el-menu-item>
      </el-menu>
    </el-header>
    <div v-if="loadingInit" class="loading-content"></div>
    <keep-alive v-else>
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
import { connect } from '@/api/detail/common/connect'
import { commonNetworkMixin } from '@/views/mixins/commonNetwork'
export default {
  name: 'Index',
  mixins: [commonNetworkMixin],
  data() {
    return {
    }
  },
  computed: {
    ip() {
      return this.$route.params.ip
    },
    activeIndex() {
      const fullpath = this.$route.path
      // */192.168.100.101/configuration/vlan/list
      const p = fullpath.match('/(?<path>monitoring|configuration|maintain|test)')
      if (p !== null) {
        return p.groups.path
      } else {
        return 'monitoring'
      }
    }
  },
  created() {
    this.loadingInit = true
    const query = {
      ip: this.ip
    }
    connect(query).then(res => {
      // console.log(res)
      this.$message({ type: 'success', message: '连接成功' })
      this.loadingInit = false
    }).catch(error => {
      console.log(error.response)
      this.$message({ type: 'error', message: '连接失败', duration: 0 })
    })
  },
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push({ path: '/equipmentsManage/detail/' + this.ip + '/' + key })
    }
  }
}
</script>

<style>
/*解决tab页超过屏幕高度不能滚动的问题, 100vh - (两头部两个的高度+10px)*/
.page-content {
    height: calc(100vh - 120px);
    overflow-y: scroll;
  }
.loading-content {
  height: 100%; width: 100%;
}
</style>
