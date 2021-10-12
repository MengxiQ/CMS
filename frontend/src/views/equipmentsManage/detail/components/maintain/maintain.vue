<template>
  <el-container>
    <el-aside :width="asideWidth">
      <div class="fold-tool">
        <span v-show="isCollapse" class="el-icon-s-unfold" @click="unfold" />
        <span v-show="!isCollapse" class="el-icon-s-fold" @click="fold" />
      </div>
      <el-menu default-active="index" :collapse="isCollapse" @open="handleOpen" @close="handleClose">
        <el-menu-item index="index">
          <i class="el-icon-cpu" />
          <span slot="title">设备维护</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <el-divider content-position="left">配置文件</el-divider>
      <el-form inline size="mini" style="margin-left: 40px">
        <el-form-item label="源配置">
          <el-select v-model="temp.source">
            <el-option label="running" value="running" />
            <el-option label="startup" value="startup" disabled />
          </el-select>
        </el-form-item>
        <el-form-item label="目标配置">
          <el-select v-model="temp.target">
            <el-option label="running" value="running" disabled />
            <el-option label="startup" value="startup" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="mini" type="primary" :disabled="loadingInit" @click="save"><i v-if="loadingInit" class="el-icon-loading" />保存</el-button>
        </el-form-item>
      </el-form>
      <el-divider content-position="left">连接管理</el-divider>
      <div style="margin-left: 40px">
        <el-button size="mini" type="danger" @click="handleDisconnect">关闭连接</el-button>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import { saveConfig } from '@/api/detail/common/saveconfig'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { detailMixins } from '@/views/equipmentsManage/detail/components/minxins/detailMixins'
import { disconnect } from '@/api/detail/common/connect'
export default {
  name: 'Maintain',
  mixins: [baseMinxin, detailMixins],
  data() {
    return {
      loadingInit: false,
      temp: {
        source: 'running',
        target: 'startup'
      }
    }
  },
  methods: {
    save() {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        source: this.temp.source,
        target: this.temp.target
      }
      saveConfig(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    },
    handleDisconnect() {
      // 关闭连接
      this.$confirm('是否关闭连接并退出？', '提示', { type: 'warning' }).then(_ => {
        const data = {
          ip: this.ip
        }
        disconnect(data).then(res => {
          // console.log(res)
          this.$message({ message: '关闭连接成功', type: 'success' })
          // 关闭当前窗口
          setTimeout(_ => {
            window.close()
          }, 1000)
        }).catch(error => {
          console.log(error)
          this.$message({ message: '关闭连接失败', type: 'error' })
        })
      }).catch(_ => {
      })
    }
  }
}
</script>

<style scoped>
.fold-tool {
  position: absolute; z-index: 1000; left: 22px; top: 22px; transition: all 0.2s;
  /*background-color: red;*/
}
.fold-tool:hover {
  cursor: pointer;
  color: rgb(64,158,255);
}
.fold-tool>span {
  font-size: 22px;
}
</style>
