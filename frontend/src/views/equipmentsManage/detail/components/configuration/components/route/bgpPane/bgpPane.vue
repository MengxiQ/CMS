<template>
  <div v-loading="loadingInit" class="pane">
    <h5 class="label-h5">进程信息
      <el-link style="margin-left: 10px" type="primary" @click="handleUpdate">编辑</el-link>
      <el-button style="float: right" size="mini" type="success" @click="getList">刷新</el-button>
    </h5>
    <divider-info :data-source="dataSource" />
    <el-row>
      <el-col :span="12"><span class="label">自治系统编号</span>
        <el-input v-if="dialogEditShow" v-model="temp.asNumber" size="mini" class="input-inline" />
        <span v-else class="props">{{ list.asNumber }}</span>
      </el-col>
      <el-col :span="12"><span class="label">状态</span>
        <el-switch
          v-if="dialogEditShow"
          v-model="temp.bgpEnable"
          active-color="#13ce66"
          inactive-color="#ff4949"
          active-value="true"
          inactive-value="false"
        />
        <span v-else class="props">
          <i v-if="list.bgpEnable === 'true'" style="color: rgb(133,206,97)" class="el-icon-success" />
          <i v-else style="color: red" class="el-icon-error" />
          {{ list.bgpEnable === 'true' ? '开' : '关' }}</span>
      </el-col>
    </el-row>
    <el-row>
      <el-col v-if="dialogEditShow" :span="24">
        <p style="font-size: smaller; color: #6f7180">tips: bgp启动和关闭需要时间，开启后请等待一会再刷新。（关闭后会清除AS号）</p>
        <el-button size="mini" type="primary" @click="handleSave">保存</el-button>
        <el-button size="mini" type="" @click="dialogEditShow = false ">取消</el-button>
      </el-col>
    </el-row>
    <el-row v-if="list.bgpEnable === 'true'">
      <el-col :span="24">
        <h5 class="label-h5">基本配置</h5>
        <el-tabs>
          <el-tab-pane lazy label="邻居列表">
            <bgp-peer :as-number="list.asNumber" />
          </el-tab-pane>
          <el-tab-pane lazy label="网络列表">
            <bgp-network :as-number="list.asNumber" />
          </el-tab-pane>
          <el-tab-pane lazy label="路由引入">
            <bgp-import :ip="ip" />
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import { getBgpBase, createBgpBase} from '@/api/detail/route/bgp/bgp-base'
import BgpPeer from '@/views/equipmentsManage/detail/components/configuration/components/route/bgpPane/componements/bgpPeer'
import BgpNetwork from '@/views/equipmentsManage/detail/components/configuration/components/route/bgpPane/componements/bgpNetwork'
import BgpImport from '@/views/equipmentsManage/detail/components/configuration/components/route/bgpPane/componements/bgpImport'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'

export default {
  name: 'BgpPane',
  components: { DividerInfo, BgpImport, BgpNetwork, BgpPeer },
  mixins: [baseMinxin],
  data() {
    return {
      importMethod: 1
    }
  },
  computed: {
  },
  methods: {
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getBgpBase(query).then(res => {
        this.list = res.data.bgpcomm.bgpSite
        this.bgpVrfs = res.data.bgpcomm.bgpVrfs
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    },
    handleUpdate() {
      this.dialogEditShow = true
      this.temp = Object.assign({}, this.list)
    },
    handleSave() {
      const data = {
        ip: this.ip,
        data: this.temp,
        source: this.$store.getters.source
      }
      createBgpBase(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    }
  }
}
</script>

<style scoped>
.pane {
  background-color: #f9f9f9;
  padding: 4px;
}

.label {
  display: inline-block;
  padding: 20px 10px;
  color: #34363b;
  min-width: 50px;
  font-size: 14px;
}

.label:after {
  content: ':';
}

.props {
  color: #3d7ed5;
  font-size: 14px;
}

.label-h5 {
  display: block;
  border-left: solid #3d7ed5 4px;
  padding: 3px 8px;
  margin: 10px 0px;
}

.input-inline {
  display: inline-block;
  width: 150px;
  height: 50px;
}
</style>
