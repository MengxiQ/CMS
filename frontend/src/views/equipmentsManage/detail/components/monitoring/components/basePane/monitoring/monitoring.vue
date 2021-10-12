<template>
  <div>
    <div>
      <el-row>
        <el-col class="col" :md="12" :xs="24">
          <system-info :ip="ip" />
        </el-col>
        <el-col class="col" :md="12" :xs="24">
          <alarm :ip="ip" />
        </el-col>
        <el-col v-if="JSON.stringify(list) === '[]'" class="col" :md="12" :xs="24">
          <pane :title="'单板'" :loading="loadingInit" @reload="getList" />
        </el-col>
        <el-col v-for="(item, key) in list" :key="key" class="col" :md="12" :xs="24">
          <board-res-states :loading="loadingInit" :data="item" @reload="getList" />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import BoardResStates from '@/views/equipmentsManage/detail/components/monitoring/components/basePane/monitoring/componements/boardResStates'
import { getBoardResStates } from '@/api/detail/monitoring/monitoring'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import SystemInfo from '@/views/equipmentsManage/detail/components/monitoring/components/basePane/monitoring/componements/systemInfo'
import { isArray } from '@/utils/isType'
import Pane from '@/components/pane/pane'
import Alarm
  from '@/views/equipmentsManage/detail/components/monitoring/components/basePane/monitoring/componements/alarm'

export default {
  name: 'Monitoring',
  components: { Alarm, Pane, SystemInfo, BoardResStates },
  mixins: [baseMinxin],
  data() {
    return {}
  },
  methods: {
    getList() {
      this.loadingInit = true
      getBoardResStates(this.ip).then(res => {
        // console.log(res)
        let boardResState = (((res.data || {}).devm || {}).boardResStates || {}).boardResState
        boardResState = isArray(boardResState) ? boardResState : Array(boardResState)
        const mpuBoards = isArray((((res.data || {}).devm || {}).mpuBoards || {}).mpuBoard) ? (((res.data || {}).devm || {}).mpuBoards || {}).mpuBoard : Array((((res.data || {}).devm || {}).mpuBoards || {}).mpuBoard)
        const lpuBoards = isArray((((res.data || {}).devm || {}).lpuBoards || {}).lpuBoard) ? (((res.data || {}).devm || {}).lpuBoards || {}).lpuBoard : Array((((res.data || {}).devm || {}).lpuBoards || {}).lpuBoard)

        // 构造数据
        const list = boardResState.map((item) => {
          const data_item = {
            isMpu: false,
            isLpu: false,
            board: item
          }
          mpuBoards.forEach(unip => {
            if (unip && item.entIndex === unip.entIndex) {
              data_item.isMpu = true
              data_item.mpu = unip
            }
          })
          lpuBoards.forEach(unip => {
            if (unip && item.entIndex === unip.entIndex) {
              data_item.isLpu = true
              data_item.lpu = unip
            }
          })
          return data_item
        })
        // console.log(list)
        this.list = list === undefined ? [] : list
        this.loadingInit = false
      }).catch(error => this.getListError(error))
    }
  }
}
</script>

<style scoped>
  .col{
    margin-bottom: 20px
  }
</style>
