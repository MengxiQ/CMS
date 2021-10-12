<template>
  <div>
    <el-row>
      <el-col :span="24" :offset="0">
        <el-steps :active="active" finish-status="success" simple>
          <el-step title="1:选择用户" />
          <el-step title="2:选择设备" />
          <el-step title="3:确认和挑选" />
        </el-steps>
        <p style="font-size: smaller;color: #97a8be; padding: 10px">tips: 批量用户指定的是用一个用户批量生产多个设备的用户。</p>
      </el-col>
    </el-row>
    <div v-show="active === 0" id="0" style="text-align: center; margin-top: 50px">
      <el-row>
        <el-col :span="22" :offset="1">
          <el-form inline size="small ">
            <el-form-item label="名称">
              <el-input v-model="query.user.username" placeholder="名称" />
            </el-form-item>
            <el-form-item label="厂商">
              <el-select v-model="query.user.device_params" clearable placeholder="厂商">
                <el-option label="华为" value="huawei" />
                <el-option label="锐捷" value="ruijie" />
                <el-option label="思科" value="cisco'" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="queryUsers">查询</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="18" :offset="3" style="border: rgb(235,238,245) 1px solid">
          <el-table
            :data="usersList"
            highlight-current-row
            @current-change="CurrentChangeUser"
          >
            <el-table-column type="index" width="20" />
            <el-table-column label="用户名" prop="username" align="center" />
            <el-table-column label="密码" prop="password" align="center" />
            <el-table-column label="端口号" prop="port" align="center" />
            <el-table-column label="设备厂商" prop="device_params" align="center" />
          </el-table>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="20" :offset="2">
          <div style="margin-top: 10px"><i class="el-icon-user-solid" />已选用户：</div>
          <el-form v-if="JSON.stringify(choicUser) !== '{}'" inline>
            <el-form-item>
              <i class="el-icon-success" style="color: green" />
            </el-form-item>
            <el-form-item label="用户名：">
              <span>{{ choicUser.username }}</span>
            </el-form-item>
            <el-form-item label="密码：">
              <span>{{ choicUser.password }}</span>
            </el-form-item>
            <el-form-item label="端口号：">
              <span>{{ choicUser.port }}</span>
            </el-form-item>
            <el-form-item label="厂商参数：">
              <span>{{ choicUser.device_params }}</span>
            </el-form-item>
            <el-form-item>
              <i class="el-icon-delete-solid delete-choice-user" title="删除选中用户" @click="choicUser = {}" />
            </el-form-item>
          </el-form>

          <div v-else style="color: rgb(192,196,204); font-size: smaller; margin-top: 10px">
            <i style="color: red" class="el-icon-error" /> 没用选中任何用户~</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12" :offset="6" style="margin-top: 10px">
          <el-button type="primary" size="small" :disabled="JSON.stringify(choicUser) === '{}'" @click="nextStep()">下一步</el-button>
        </el-col>
      </el-row>

    </div>
    <div v-show="active === 1" id="1" style="text-align: center; margin-top: 50px">
      <el-row>
        <el-col :span="20" :offset="2">
          <el-form size="mini" :inline="true">
            <el-form-item label="起始IP:">
              <el-input v-model="query.equipment.beginIP" placeholder="起始IP" />
            </el-form-item>
            <el-form-item label="结束IP:">
              <el-input v-model="query.equipment.endIP" placeholder="结束IP" />
            </el-form-item>
            <el-form-item label="厂商">
              <el-select v-model="query.equipment.vendor" clearable placeholder="厂商">
                <el-option label="华为" value="huawei" />
                <el-option label="锐捷" value="ruijie" />
                <el-option label="思科" value="cisco'" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button icon="el-icon-search" type="primary" @click="queryEquipments">查询</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="20" :offset="2">
          <el-table
            ref="multipleTable"
            :data="equipmentsList"
            tooltip-effect="dark"
            style="width: 100%"
            height="200"
            @selection-change="SelectionEquipemntChange"
          >
            <el-table-column
              type="selection"
              width="55"
            />
            <el-table-column
              label="IP"

              prop="ip"
            />
            <el-table-column
              prop="name"
              label="名称"
            />
            <el-table-column
              prop="type.name"
              label="类型"
            />
            <el-table-column
              prop="unittype.name"
              label="型号"
            />
          </el-table>
        </el-col>
      </el-row>
      <el-row style="margin-top: 10px">
        <el-col :span="20" :offset="2">
          <el-button type="" size="small" @click="previousStep()">上一步</el-button>
          <el-button :disabled="JSON.stringify(choicEquipments) === '[]' " type="primary" size="small" @click="nextStep()">下一步</el-button>
        </el-col>
      </el-row>
    </div>
    <div v-show="active === 2" id="3" style="margin-top: 50px">
      <el-row>
        <el-col :span="20" :offset="2">
          <el-form inline>
            <el-form-item label="用户名：">
              <span>{{ choicUser.username }}</span>
            </el-form-item>
            <el-form-item label="密码：">
              <span>{{ choicUser.password }}</span>
            </el-form-item>
            <el-form-item label="端口号：">
              <span>{{ choicUser.port }}</span>
            </el-form-item>
            <el-form-item label="厂商参数：">
              <span>{{ choicUser.device_params }}</span>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="20" :offset="2">
          <el-transfer
            v-model="targetData"
            filterable
            :titles="['可选设备', '已选设备']"
            :button-texts="['到左边', '到右边']"
            :props="{
              key: 'id',
              label: 'name'
            }"
            :data="choicEquipments"
          />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="20" :offset="2">
          <el-button type="" size="small" @click="previousStep()">上一步</el-button>
          <el-button :disabled="JSON.stringify(targetData) === '[]'" type="primary" size="small" @click="complete()">完成</el-button>
        </el-col>
      </el-row>
    </div>
    <div v-show="active === 3" id="4" style="margin-top: 50px">
      <div style="width: 100%; height: 100%; text-align: center;margin-top: 100px">
        <div v-if="success === true" id="success">
          <i class="el-icon-success" style="font-size: 30px; color: green">success</i>
        </div>
        <div v-else id="error">
          <i class="el-icon-error" style="font-size: 30px; color: red">error</i>
        </div>
        <el-button size="small" type="primary" style="margin-top:10px" @click="again">再次批量</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchList, batchUsers } from '@/api/netconfUsers'
import { fetchEquipmentListByIp } from '@/api/equipment'

export default {
  name: 'Index',
  data() {
    return {
      query: {
        user: {
          username: '',
          device_params: ''
        },
        equipment: {
          beginIP: '',
          endIP: '',
          vendor: ''
        }
      },
      active: 0,
      usersList: [],
      choicUser: {},
      equipmentsList: [],
      choicEquipments: [],
      targetData: [], // key值的数组（设备id）
      targerEquipments: [], // 选中的用户
      success: false// 是否成功
    }
  },
  methods: {
    nextStep() {
      if (this.active < 3) {
        this.active += 1
      }
    },
    previousStep() {
      if (this.active > 0) {
        this.active -= 1
      }
    },
    complete() {
      const data = {
        equipmentsIdList: this.targetData,
        choicUser: this.choicUser
      }
      batchUsers(data).then(res => {
        this.$message({ type: 'success', message: '批量成功' })
        this.success = true
        if (this.active < 3) {
          this.active += 1
        }
      }).catch(erroe => {
        this.$message({ type: 'error', message: '批量失败' })
        this.success = false
        if (this.active < 3) {
          this.active += 1
        }
      })
    },
    CurrentChangeUser(currentRow) {
      this.choicUser = Object.assign({}, currentRow)
    },
    SelectionEquipemntChange(val) {
      this.choicEquipments = val
    },
    queryUsers() {
      fetchList(this.query.user).then(res => {
        this.usersList = res
      }).catch()
    },
    queryEquipments() {
      fetchEquipmentListByIp(this.query.equipment).then(res => {
        this.equipmentsList = res
      }).catch()
    },
    again() {
      // 清除数据
      this.choicUser = {}
      this.choicEquipments = []
      this.equipmentsList = []
      this.targetData = []
      this.active = 0
    },
    log() {
      // // 过滤出选中的ID的条目
      // let data = this.choicEquipments.filter((item, key) => {
      //   return (this.targetData.indexOf(item.id)) !== -1
      //
      // })
      // console.log(data)
      // // # data 就是要选中的对象列表
    }
  }
}
</script>

<style scoped>
  .delete-choice-user{
    color: red;
    margin-left: 20px;
  }
  .delete-choice-user:hover{
    transform: scale(1.1);
    cursor: pointer;
  }
</style>
