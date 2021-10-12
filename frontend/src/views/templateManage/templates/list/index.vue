<template>
  <div class="app-container">
    <el-button-group style="float: left">
      <el-button
        size="small"
        class="filter-item"
        type="primary"
        icon="el-icon-edit"
        @click="handleCreate"
      >
        添加
      </el-button>
      <el-button
        size="small"
        class="filter-item"
        type="success"
        icon="el-icon-refresh"
        @click="handlerefresh"
      >
        刷新
      </el-button>
    </el-button-group>
    <div class="filter-container">
      <el-input
        v-model="listQuery.name"
        size="small"
        placeholder="模板名称"
        style="width: 200px;"
        class="filter-item"
      />
      <el-select
        v-model="listQuery.tempType"
        filterable
        clearable
        size="small"
        placeholder="模板类型"
        class="filter-item"
        style="width: 160px"
      >
        <el-option
          v-for="(item, key) in this.$store.getters.templateTypes"
          :key="key"
          :label="item.name"
          :value="item.id"
        />
      </el-select>
      <el-button v-waves size="small" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
    </div>
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <!--      展开行-->
      <!--      <el-table-column type="expand">-->
      <!--        <div slot="header" slot-scope=""><i class="el-icon-view" /></div>-->
      <!--        <template slot-scope="props">-->
      <!--          <el-form label-position="left" class="demo-table-expand">-->
      <!--            <el-form-item label="支持设备:">-->
      <!--              <span-->
      <!--                v-for="(item , key) in props.row.support"-->
      <!--                :key="key"-->
      <!--                class="support-item"-->
      <!--              >{{ item }}</span>-->
      <!--            </el-form-item>-->

      <!--            <el-form-item label="模板功能:">-->
      <!--              <div>{{ props.row.function ? props.row.function.name : 'null' }}-->
      <!--              </div>-->
      <!--            </el-form-item>-->
      <!--            <el-form-item label="模板描述:">-->
      <!--              <div>{{ props.row.remark }}</div>-->
      <!--            </el-form-item>-->
      <!--            <el-form-item label="模板参数:">-->
      <!--              <el-row>-->
      <!--                <el-col v-for="(item, key) in props.row.params_set" :key="key" :span="24">-->
      <!--                  <span class="show-param-item">参数{{ key + 1 }}：{{ item.name }}</span>-->
      <!--                  <span class="show-param-item">描述：{{ item.remark }}</span>-->
      <!--                  <span class="show-param-item">约束：{{ item.constraint }}</span>-->
      <!--                </el-col>-->
      <!--              </el-row>-->
      <!--            </el-form-item>-->
      <!--          </el-form>-->
      <!--          <h4>模板内容：</h4>-->
      <!--          <template-edit class="code-block" :template="props.row" :read-only="true" />-->

      <!--        </template>-->
      <!--      </el-table-column>-->
      <!--      -->
      <el-table-column
        label="模板名称"
        prop="name"
        align="center"
        :class-name="getSortClass('id')"
      />
      <el-table-column
        label="模板类型"
        prop="tempType.name"
        align="center"
        :class-name="getSortClass('id')"
      />
      <el-table-column
        label="模板功能"
        prop="function.name"
        align="center"
        :class-name="getSortClass('id')"
      />
      <el-table-column label="最后更新" align="center">
        <template slot-scope="{row}">
          <span>{{ parseTime(new Date(Date.parse(row.updateDate))) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="模板内容" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleEditTemplate(row)">编辑</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="150" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button-group>
            <el-button type="" size="mini" @click="handleUpdate(row)">
              编辑
            </el-button>
<!--            <el-button size="mini" type="danger" @click="handleDelete(row,$index)">-->
<!--              删除-->
<!--            </el-button>-->
             <el-popconfirm
              title="确定删除吗？"
              @onConfirm="handleDelete(row,$index)"
            >
              <el-button
                slot="reference"
                size="mini"
                type="danger"
              >删除
              </el-button>
            </el-popconfirm>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="60%" :before-close="clsotEditDialog">
      <div class="form-content">
        <el-form ref="dataForm" label-position="left" label-width="80px">
          <el-form-item label="模板名称">
            <el-input v-model="temp.name" class="input-item" />
          </el-form-item>
          <el-form-item label="模板类型">
            <el-select
              v-model="temp.tempType"
              class="input-item"
              filterable
              placeholder="Please select"
            >
              <el-option
                v-for="(item, key) in this.$store.getters.templateTypes"
                :key="key"
                :label="item.name"
                :value="item.name"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="支持型号">
            <el-select
              v-model="temp.support"
              class="input-item"
              multiple
              filterable
            >
              <el-option
                v-for="(item, key) in this.$store.getters.unitTypes"
                :key="key"
                :label="item.name"
                :value="item.name"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="模板功能">
            <el-select
              v-model="temp.function"
              class="input-item"
              filterable
              :placeholder="'select'"
            >
              <el-option
                v-for="(item, key) in this.$store.getters.functionTypes"
                :key="key"
                :label="item.name"
                :value="item.name"
              >
                <span style="float: left; margin-right: 20px"> {{ item.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px ">{{ item.remark }}</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="最后更新">
            <el-date-picker v-model="temp.updateDate" class="input-item" type="datetime" placeholder="Please pick a date" />
          </el-form-item>
          <el-form-item label="模板描述">
            <el-input v-model="temp.remark" class="input-item" type="textarea" />
          </el-form-item>
          <!--          :(动态添加表单) # 核验xml data中是否有$(参数)-->
          <h4>模板参数</h4>
          <el-row v-for="(item, key) in temp.params" :key="key" class="param-content">
            <el-col :span="24">
              <i>P</i>参数{{ key + 1 }}
              <el-dropdown trigger="click" style="margin-left: 10px;">
                <span class="el-dropdown-link">
                  {{ item.role === null ? 'left' : item.role }}<i class="el-icon-arrow-down el-icon--right" />
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="changeRole(key,'key')">Key</el-dropdown-item>
                  <el-dropdown-item @click.native="changeRole(key,'left')">Leaf</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
              <i class="el-icon-delete-solid param-item-delete" />
            </el-col>
            <el-col :span="24">
              <label class="param-item">名称
                <el-input v-model="item.name" class="param-item-input" size="mini" />
              </label>
              <label class="param-item">标签
                <el-input v-model="item.label" class="param-item-input" size="mini" />
              </label>
            </el-col>
            <el-col :span="24">
              <label class="param-item">描述
                <el-input v-model="item.remark" class="param-item-input" size="mini" placeholder="可选" />
              </label>
              <label class="param-item">约束
                <el-input v-model="item.constraint" class="param-item-input" size="mini" placeholder="参数约束" />
              </label>
            </el-col>
          </el-row>
          <el-button
            title="添加模板参数"
            size="mini"
            type="primary"
            icon="el-icon-plus"
            style="margin-bottom: 10px;"
            @click="handleAddParam"
          >参数</el-button>
          <el-form-item label="数据位置">
            <el-input v-model="temp.position" class="input-item" />
          </el-form-item>
          <h4>模板内容</h4>
          <div style="border:1px solid #bfcbd9">
            <template-edit :template="temp" :read-only="false" />
          </div>
        </el-form>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

    <el-dialog title="编辑模板" :visible="isEditTemplate" width="90%" @close="isEditTemplate = false">
      <!--      <h1 style="position:absolute; margin: 0;padding: 0;width: 100%;text-align: left;font-size: 17px;font-weight: normal;height: 20px">{{ativeTemplate.name}}</h1>-->
      <template slot="title">编辑模板: <span style="font-weight: bold; color: #3d7ed5">{{ ativeTemplate.name }}</span>
      </template>
      <template-edit class="code-block" :template="ativeTemplate" :read-only="false" />
      <div slot="footer" class="dialog-footer">
        <el-button size="mini" @click="isEditTemplate = false">
          取消
        </el-button>
        <el-button size="mini" type="primary" @click="saveTemplate">
          保存
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getTemplatesList, saveTemplate, addTemplate, deleteTemplate, updateTemplate } from '@/api/configManage/templates'
import TemplateEdit from '@/views/templateManage/templates/edit/index'
import { commonOperationMixin } from '@/views/mixins/commonOperationMixin'

export default {
  name: 'TemplatesList',
  components: { TemplateEdit, Pagination },
  directives: { waves },
  mixins: [commonOperationMixin],
  data() {
    return {
      // 编辑模板
      isEditTemplate: false,
      ativeTemplate: { templateData: '' },
      //
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        ip: undefined,
        name: undefined,
        tempType: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        name: '',
        tempType: '',
        support: [],
        updateDate: new Date(),
        function: null,
        position: null,
        params: [{ name: null, remark: null, constraint: null, role: 'left' }],
        templateData: '<-- 开始编辑你的模板内容!-->'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '更新模板信息',
        create: '创建模板'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        // type: [{ required: true, message: 'type is required', trigger: 'change' }],
        // timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        // title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    // this.$store.dispatch('getTypes')
  },
  methods: {
    parseTime(time, format) {
      return parseTime(time, format)
    },
    changeRole(key, role) {
      // console.log(key, role)
      this.temp.params[key].role = role
      this.$forceUpdate()
    },
    // 删除参数属性
    deleteParam(key) {
      console.log(key)
      this.temp.params.splice(key, 1)
    },
    // 关闭编辑对话框
    clsotEditDialog() {
      this.beforeDialogClose(this.resetTemp)
    },
    // 点击新增参数
    handleAddParam() {
      this.temp.params.push({ name: '', remark: '' })
    },
    // 保存模板
    saveTemplate() {
      console.log(this.ativeTemplate)
      saveTemplate(this.ativeTemplate).then(res => {
        console.log('res', res)
        this.isEditTemplate = false
        this.ativeTemplate = { templateData: '' }
        this.$message({ type: 'success', message: '保存成功' })
      }).catch()
    },
    handleEditTemplate(row) {
      this.ativeTemplate = row
      this.isEditTemplate = true
    },
    handlerefresh() {
      this.getList()
    },
    gotoDetail(row) {
      this.$router.push({
        path: '/equipmentsManage/detail/' + row.ip
        // query: {
        //   ip: ,
        //   mac: row.mac
        // }
      })
    },
    getList() {
      this.listLoading = true
      getTemplatesList(this.listQuery).then(response => {
        if (response !== null) {
          this.list = response.results
          this.total = response.count
          this.listLoading = false
        } else {
          return null
        }
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.dialogFormVisible = false
      this.temp = {
        name: '',
        tempType: '',
        support: [],
        updateDate: new Date(),
        function: null,
        params: [{ name: '', remark: '', constraint: null }],
        templateData: '<?xml version="1.0" encoding="utf-8" ?>\n' +
          '<tempalte>\n' +
          '    <tempalte-get>\n' +
          '        <filter type="subtree">\n' +
          '        </filter>\n' +
          '    </tempalte-get>\n' +
          '    \n' +
          '    <tempalte-merge>\n' +
          '    <config>\n' +
          '    </config>\n' +
          '    </tempalte-merge>\n' +
          '    \n' +
          '    <tempalte-delete>\n' +
          '    <config>\n' +
          '    </config>\n' +
          '    </tempalte-delete>\n' +
          '</tempalte>'
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      // this.$nextTick(() => {
      //   this.$refs['dataForm'].clearValidate()
      // })
    },
    createData() {
      addTemplate(this.temp).then(respon => {
        this.dialogFormVisible = false
        // 或许不用刷新，可以直接append返回的数据
        this.handlerefresh()
        this.$notify({
          title: 'Success',
          message: '创建成功',
          type: 'success',
          duration: 2000
        })
      }).catch(reason => {
        console.log(reason)
        this.$notify({
          title: 'Fault',
          message: '创建失败',
          type: 'danger',
          duration: 2000
        })
      })
    },
    handleUpdate(row) {
      const data = Object.assign({}, row)
      data.function = data.function.name
      const params = data.params_set
      const tempType = data.tempType.name
      data.params = params
      data.tempType = tempType
      delete data.params_set

      this.temp = Object.assign({}, data) // copy obj
      //
      // this.temp = row
      // console.log(this.temp)
      // delete this.temp.params_set

      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      // this.$nextTick(() => {
      //   this.$refs['dataForm'].clearValidate()
      // })
    },
    updateData() {
      updateTemplate(this.temp).then(res => {
        // const index = this.list.findIndex(v => v.id === this.temp.id)
        // this.list.splice(index, 1, this.temp)
        this.getList()
        this.dialogFormVisible = false
        this.$notify({
          title: 'Success',
          message: '更新成功',
          type: 'success',
          duration: 2000
        })
      }).catch(error => {
        console.log(error)
        this.$notify({
          title: 'Faults',
          message: '更新失败',
          type: 'danger',
          duration: 2000
        })
      })
    },
    handleDelete(row, index) {
      deleteTemplate(row.id).then(reason => {
        this.$notify({
          title: 'Success',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
        this.list.splice(index, 1)
      }).catch(reason => {
        this.$notify({
          title: 'Faults',
          message: '删除失败',
          type: 'danger',
          duration: 2000
        })
      })
    },
    handleFetchPv(pv) {
      // fetchPv(pv).then(response => {
      //   this.pvData = response.data.pvData
      //   this.dialogPvVisible = true
      // })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
<style lang="scss" scoped>
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
.form-content {
  margin: 0 auto;
}
.input-item {
  width: 90%;
}
.code-block {
  border: 1px solid rgb(191, 203, 217);
}

.show-param-item {
  padding: 5px;
}
.param-content {
  padding: 10px;
}
.param-item {
  font-weight: normal;
  display: inline-block;
  margin: 10px;
}
.param-item-delete {
  color: red;
  margin-left: 20px;
}
.param-item-delete:hover {
  cursor: pointer;
}
.param-item-input {
  display: inline-block;
  width: 200px;
  margin-left: 10px;
}

.filter-container {
  //padding: 10px;
  float: right;
}

.filter-item {
  //margin-right: 5px;
}

.dialog_content {
  display: inline-block;
  width: 50%;
  padding: 0 20px;

}

.left {
  float: left;
  border-right: rgb(52, 153, 215) dashed 1px;
}

.right {
  float: right;
}

.dialog_body {
  height: 500px;
}

.dialog_title {
  color: #313131;
}

.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;

}

.support-item {
  margin: 0 20px 0 0;
  //background: red;
  //line-height: 25px;
  ////height: 25px;
}

.code {
  border: 1px solid rgb(235, 238, 245);
  background-color: #f9f9f9;
  color: #2b2f3a;
  padding: 5px;
}
</style>
