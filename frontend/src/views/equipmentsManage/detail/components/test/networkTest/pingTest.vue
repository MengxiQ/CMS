<template>
  <div>
    <pingchart v-if="isShowChart" :active-data="activeData" @back="onBack" :key="chartKey" @refresh="refreshChart" />
    <div v-else>
      <el-row>
        <el-col :span="24">
          <el-button-group>
            <el-button size="mini" type="primary" @click="handleCreate">新建</el-button>
            <el-button size="mini" type="success" @click="getList">刷新</el-button>
          </el-button-group>
          <span style="font-size: 12px; color: #bfcbd9">（只能在Schema模式下使用）</span>
        </el-col>
      </el-row>
      <el-table v-loading="loadingInit" :data="isArray(list) ? list : Array(list)">
        <el-table-column align="center" label="名称" prop="testName" />
        <el-table-column align="center" label="发送包" prop="packetSend" />
        <el-table-column align="center" label="接收包" prop="packetRecv" />
        <el-table-column align="center" label=" rttMin" prop="rttMin">
          <template slot-scope="props">
            <span>{{ props.row.rttMin + 'ms' }}</span>
          </template>
        </el-table-column>><!-- 报文最大往返时间 -->
        <el-table-column align="center" label="rttMax" prop="rttMax">
          <template slot-scope="props">
            <span>{{ props.row.rttMax + 'ms' }}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="测试状态" prop="status">
          <template slot-scope="props">
            <el-tag v-if="props.row.status === 'processing'" size="mini" type="warning">{{ props.row.status }}</el-tag>
            <el-tag v-else size="mini" type="primary">{{ props.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column align="center" label="丢包率" prop="lossRatio">
          <template slot-scope="props">
            <el-tag v-if="parseInt(((props.row || {}).lossRatio || '').match('^[0-9]*')[0]) >= 50" size="mini" type="danger">{{ props.row.lossRatio }}%</el-tag>
            <el-tag v-if="(parseInt(((props.row || {}).lossRatio || '').match('^[0-9]*')[0]) > 0) && (parseInt(props.row.lossRatio.match('^[0-9]*')[0]) < 50)" size="mini" type="primary">{{ props.row.lossRatio }}%</el-tag>
            <el-tag v-if="parseInt(((props.row || {}).lossRatio || '').match('^[0-9]*')[0]) === 0" size="mini" type="success">{{ props.row.lossRatio }}%</el-tag>
          </template>
        </el-table-column>
        <!--      <el-table-column align="center" label="结果" prop="errorType" >-->
        <!--        <template slot-scope="props">-->
        <!--          <el-tag v-if="props.row.errorType === 'success'" size="mini" type="success">{{ props.row.errorType }}</el-tag>-->
        <!--          <el-tag v-else size="mini" type="error">{{ props.row.errorType }}</el-tag>-->
        <!--        </template>-->
        <!--      </el-table-column>-->
        <el-table-column align="center" label="操作" prop="" width="140">
          <template slot-scope="scope">
            <el-button-group>
              <el-button size="mini" type="primary" @click="showChart(scope.row)">详情</el-button>
              <!--            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>-->
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog :title="textMap[dialogEditStatus]" :visible.sync="dialogEditShow" width="70%" :before-close="beforCloseDialog">
        <edit :params="params" @cancel="dialogEditShow = false" @save="handleSave"></edit>
        <!--        <el-form style="width: 500px; margin: auto" label-position="right" label-width="120px" size="mini">-->
<!--          <el-form-item-->
<!--            v-for="(item, key) in params"-->
<!--            :key="key"-->
<!--            style="position: relative; padding: 0px 0 20px 0"-->
<!--            :label="item.name"-->
<!--            size="medium"-->
<!--          >-->
<!--            <div style="position: absolute;z-index: 100;top: -28px; font-size: smaller; color: #5a5e66">{{ item.remark }}-->
<!--              <span style="margin-left: 5px;color: #3d7ed5">({{ item.constraint }})</span></div>-->
<!--            <el-select-->
<!--              v-if="(item.constraint).match('CHIOCE<(?<p>.*)>')"-->
<!--              v-model="temp[item.name]"-->
<!--            >-->
<!--              <el-option-->
<!--                v-for="(i, k) in constraint(item.constraint)"-->
<!--                :key="k"-->
<!--                :value="i"-->
<!--                :label="i"-->
<!--              />-->
<!--            </el-select>-->
<!--            <el-switch-->
<!--              v-if="item.constraint === 'BOOLEAN'"-->
<!--              v-model="temp[item.name]"-->
<!--              active-color="#13ce66"-->
<!--              inactive-color="#ff4949"-->
<!--              :active-value="false"-->
<!--              :inactive-value="true"-->
<!--            />-->
<!--            <el-input-->
<!--              v-if="item.constraint.match('INT<?(?<p>.*)>?') || item.constraint === 'IP' || item.constraint === 'MASK' || item.constraint === 'WILDCARD' || item.constraint === 'STRING'"-->
<!--              v-model="temp[item.name]"-->
<!--              :disabled="item.name === 'processId'"-->
<!--            />-->
<!--          </el-form-item>-->
<!--          <el-form-item>-->
<!--            <el-button type="primary" size="mini" @click="handleSave">新建</el-button>-->
<!--          </el-form-item>-->
<!--        </el-form>-->
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { getPingResult, creataPingTest, deletePingTest } from '@/api/detail/test/ping'
import { getNext } from '@/api/detail/common/getNext'
import { baseMinxin } from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/baseMixin'
import Pingchart from '@/views/equipmentsManage/detail/components/test/networkTest/pingchart'
import { isArray } from '@/utils/validate'
import Edit from '@/views/equipmentsManage/detail/components/configuration/components/Mixin/edit'
export default {
  name: 'PingTest',
  components: { Edit, Pingchart },
  mixins: [baseMinxin],
  data() {
    return {
      chartKey: 0,
      isShowChart: false,
      activeData: {},
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: 'Edit',
        create: '新建ping测试任务'
      }
    }
  },
  methods: {
    refreshChart() {
      this.chartKey += 1
    },
    showChart(item) {
      this.activeData = item
      this.isShowChart = true
    },
    onBack() {
      this.isShowChart = false
    },
    getList() {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source
      }
      getPingResult(query).then(res => {
        // console.log(res)
        if (res.data !== null) {
          const result = res.data.dgntl.ipv4.ipv4PingResults.ipv4PingResult
          // 转换成数组
          this.list = this.isArray(result) ? result : Array(result)
          this.getListSuccess(res, query)
          const setId = res.data.setId
          if (setId !== undefined && setId !== null) {
            this.getNextData(setId)
            // this.$confirm('获取更多(' + setId + ')？')
            //   .then(_ => {
            //     console.log('setId', setId)
            //     this.getNextData(setId)
            //   })
            //   .catch(_ => {})
          }
        } else {
          this.getListSuccess(res, query)
          this.list = []
        }
      }).catch(error => this.getListError(error))
    },
    getNextData(setId) {
      this.loadingInit = true
      const query = {
        ip: this.ip,
        source: this.$store.getters.source,
        setId: setId
      }
      getNext(query).then(res => {
        // console.log(res)
        if (res.data !== null) {
          let result = (((((res || {}).data || {}).dgntl || {}).ipv4 || {}).ipv4PingResults || {}).ipv4PingResult
          // 转换成数组
          result = isArray(result) ? result : Array(result)
          // pingResultDetails.pingResultDetail
          // console.log('next:', result)
          this.list.forEach(item => {
            // console.log(result.testName)
            result.forEach(result_item => {
              if (item.testName === result_item.testName) {
                // console.log('0')
                // 如果是同一对象，拼接数组
                item.pingResultDetails.pingResultDetail.push.apply(item.pingResultDetails.pingResultDetail, result_item.pingResultDetails.pingResultDetail)
              // console.log('1')
              } else {
                // 如果不等于就是有发过来新的对象
                // 检查list是否否有该对象了
                let flag = false
                this.list.forEach(i => {
                  if (result_item.testName === i.testName) {
                    // 有了该对象
                    flag = true
                  }
                })
                if (!flag) {
                  // 如果还没有对象，创建对象
                  this.list.push(result_item)
                }
              }
            })
          })
          const setId = res.data.setId
          if (setId !== undefined && setId !== null) {
            this.getNextData(setId)
            // this.$confirm('获取更多(setID:' + setId + ')？')
            //   .then(_ => {
            //     console.log('get->setId', setId)
            //     this.getNextData(setId)
            //   })
            //   .catch(_ => {
            //     console.log('complete')
            //     this.loadingInit = false
            //   })
          } else {
            console.log('complete')
            this.loadingInit = false
          }
        } else {
          this.getListSuccess(res, query)
          this.list = []
        }
      }).catch(error => this.getListError(error))
    },
    handleSave(temp) {
      this.loadingInit = true
      const data = {
        ip: this.ip,
        data: temp,
        source: this.$store.getters.source
      }
      creataPingTest(data).then(res => this.createSuccess()).catch(error => this.createError(error))
    }
  }
}
</script>

<style scoped>

</style>
