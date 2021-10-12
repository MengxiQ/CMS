<template>
  <div v-loading="loadingInit">
    <el-button-group style="position: absolute; z-index: 1000; right: 10px; top: 10px">
      <el-button type="primary" size="mini" @click="handleCreate">新建</el-button>
      <el-button type="success" size="mini" @click="getList">刷新</el-button>
    </el-button-group>
    <divider-info :data-source="dataSource" />
    <el-tabs
      v-if="JSON.stringify(list) !== '[]'"
      v-model="activeName"
      type="border-card"
      editable
      @edit="handleTabsEdit"
      @tab-click="handleClickTab"
    >
      <el-tab-pane
        v-for="(item, key) in list"
        :key="key"
        lazy
        :label="'进程'+ item.processId"
        :name="item.processId"
      >
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="" name="1">
            <template slot="title">
              <i class="el-icon-info" style="margin-right: 5px" />
              <span style="margin-right: 10px">进程信息</span>
              <el-link title="编辑" type="primary" class="el-icon-edit" @click.native.stop="handleUpdate(item)" />
            </template>
            <ospf-process :item="item" />
          </el-collapse-item>
          <el-collapse-item title="" name="2">
            <template slot="title">
              <i class="el-icon-map-location" style="margin-right: 5px" />区域列表
            </template>
            <ospf-area :process-id="item.processId" />
          </el-collapse-item>
        </el-collapse>
      </el-tab-pane>
    </el-tabs>
    <el-table v-else :data="[]" />

    <!-- 编辑进程对话框-->
    <el-dialog :title="textMap[dialogEditStatus]" :visible="dialogEditShow">
      <edit :params="params" :default_temp="defaultTemp()" @save="handleSave" @cancel="dialogEditShow = false" />
    </el-dialog>
  </div>

</template>

<script>
import { deleteOspfProcess } from '@/api/detail/route/ospf/ospfProcess'
import { createOspfProcess, getOspfProcess } from '@/api/detail/route/ospf/ospfProcess'
import { isArray } from '@/utils/isType'
import OspfProcess from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfPane/componements/ospfProcess'
import OspfArea from '@/views/equipmentsManage/detail/components/configuration/components/route/ospf/ospfPane/componements/ospfArea/ospfArea'
import DividerInfo from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/divider-info'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'

export default {
  name: 'OspfPane',
  components: { Edit, DividerInfo, OspfArea, OspfProcess },
  mixins: [baseMinxin],
  data() {
    return {
      ativeItem: {},
      activeName: null,
      activeCollapse: ['1']
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    handleTabsEdit(targetName, action) {
      // console.log(targetName, action)
      switch (action) {
        case 'add': { this.handleCreate(); break }
        case 'remove': { this.handleDelete({ processId: targetName }); break }
      }
    },
    handleSave(temp) {
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      createOspfProcess(data).then(res => {
        this.$message({ type: 'success', message: '配置成功。' })
        this.getList()
        this.dialogEditShow = false
      }).catch(error => {
        this.$message({ type: 'error', message: error.response.data['msg'] })
      })
    },
    beforCloseDialog() {
      this.dialogEditShow = false
    },
    handleClickTab(tab, event) {
      // console.log(tab, event)
      // console.log(this.activeName)
      this.$router.push({ query: { processId: this.activeName }})
    },
    getListError(error) {
      console.log(error)
      // console.log(error.response)
      // 尝试获取后台报错信息
      if (((error.response || {}).data || {}).msg) {
        const data = error.response.data
        // console.log(data.msg)
        if (data.msg.match('candidate data store does not exist.') !== null) {
          // 候选数据没有创建
          this.list = []
          this.dataSource = this.$store.getters.source
          this.$message({ type: 'info', message: '开始配置并创建candidate数据库.' })
        } else {
          this.$message({ type: 'error', message: data.msg })
        }
      } else {
        // 获取不到后台报错信息
        this.$message({ type: 'error', message: ' 请求失败，请尝试刷新.' })
      }
      // 关闭加载提示
      this.loadingInit = false
    },
    getList() {
      this.list = []
      this.loadingInit = true
      // const promiseArr = [
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getOspfProcess(query).then(res => {
        this.params = res.params
        if (res.data !== null) {
          // if (isArray(res.data.ospfv2.ospfv2comm.ospfSites.ospfSite)) {
          //   this.list = res.data.ospfv2.ospfv2comm.ospfSites.ospfSite
          // } else {
          //   this.list = Array(res.data.ospfv2.ospfv2comm.ospfSites.ospfSite)
          // }
          const data = res.data ? res.data : []
          this.list = isArray(data) ? data : Array(data)
          // this.activeName = this.list[0].processId
          // 设置打开的ospf进程
          this.activeName = this.$route.query.processId
          // 如果为undefined 打开第一个进程
          if (this.activeName === undefined) {
            this.activeName = this.list[0].processId
          }
        }
        this.loadingInit = false
        this.dataSource = query.source
      }).catch(errpr => this.getListError(errpr))
    },
    handleDelete(row) {
      this.$confirm('是否删除OSPF进程:' + row.processId, '删除OSPF进程', { type: 'warning' }).then(_ => {
        const data = {
          ip: this.ip,
          data: row,
          source: this.$store.getters.source
        }
        deleteOspfProcess(data).then(res => {
          this.$message({ type: 'success', message: '配置成功。' })
          this.getList()
        }).catch(error => {
          this.$message({ type: 'error', message: error.response.data['msg'] })
        })
      }).catch(_ => {})
    }
  }
}
</script>

<style scoped>
.label-h5 {
  border-left: solid #3d7ed5 4px;
  padding-left: 4px;
}
</style>
