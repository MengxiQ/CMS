<template>
  <div>
    <div class="">
      <div>
        <el-radio-group v-model="configMode" size="mini">
          <el-radio-button label="系统模板" />
          <el-radio-button label="自定义模板" />
        </el-radio-group>
      </div>
      <div v-if="configMode === '系统模板'">
        <el-row>
          <el-col class="left" :span="24">
            <el-input
              v-model="listQuery.name"
              size="small"
              placeholder="模板名称"
              style="width: 200px;"
              class="filter-item"
              @keyup.enter.native="handleFilter"
            />
            <el-select
              v-model="listQuery.tempType"
              size="small"
              placeholder="模板类型"
              clearable
              filterable
              class="filter-item"
              style="width: 130px"
            >
              <el-option
                v-for="(item, key) in this.$store.getters.templateTypes"
                :key="key"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
            <el-button size="small" type="primary" icon="el-icon-search" @click="handleFilter">
              搜索
            </el-button>
            <el-table
              v-loading="listLoading"
              :data="list"
              fit
              highlight-current-row
              height="300"
              @current-change="handleCurrentChange"
            >
              <!--      展开行-->
              <el-table-column v-if="false" type="expand">
                <div slot="header" slot-scope=""><i class="el-icon-view" /></div>
                <template slot-scope="props">
                  <el-form label-position="left" class="demo-table-expand" size="mini">
                    <el-form-item label="支持设备:">
                      <span
                        v-for="(item , key) in props.row.support"
                        :key="key"
                        class="support-item"
                      >{{ item }}</span>
                    </el-form-item>

                    <el-form-item label="模板功能:">
                      <div>命令：{{ props.row.function ? props.row.function.name : 'null' }}&nbsp; &nbsp; # &nbsp;
                        &nbsp;{{ props.row.function ? props.row.function.remark : 'null' }}
                      </div>
                    </el-form-item>
                    <el-form-item label="模板描述:">
                      <div>{{ props.row.remark }}</div>
                    </el-form-item>
                    <el-form-item label="模板参数:">
                      <el-row>
                        <el-col v-for="(item, key) in props.row.params_set" :key="key" :span="24">
                          <span class="show-param—item">参数{{ key + 1 }}：{{ item.name }}</span>
                          <span class="show-param—item">描述：{{ item.remark }}</span>
                          <span class="show-param—item">约束：{{ item.constraint }}</span>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-form>
                  <h4>模板内容：</h4>
                  <!--          <pre class="code">-->
                  <!--              {{props.row.templateData.trim()}}-->
                  <!--          </pre>-->
                  <template-edit class="code-block" :template="props.row" :read-only="true" />
                </template>
              </el-table-column>
              <!--      -->
              <el-table-column
                label="模板名称"
                prop="name"
                align="center"
              />
              <el-table-column
                label="模板类型"
                prop="tempType.name"
                align="center"
              />
              <el-table-column
                label="模板功能"
                prop="function.name"
                align="center"
              />
            </el-table>
          </el-col>
          <el-col class="right" :span="24">
            <el-collapse style="padding: 0 20px">
              <el-collapse-item>
                <template slot="title">
                  <div style="width:100%; text-align: center">
                    <div style="display: inline-block"><i class="el-icon-user-solid" />已选模板：</div>
                    <ul
                      v-if="JSON.stringify(selectedtemplate) !== '{}'"
                      class="select-title-ul"
                      style="display: inline-block"
                    >
                      <li class="select-title-li">
                        <i class="el-icon-success" style="color: green" />
                      </li>
                      <li class="select-title-li">
                        模板名称：<span>{{ selectedtemplate.name }}</span>
                      </li>
                      <li class="select-title-li">
                        模板类型：<span>{{ selectedtemplate.tempType.name }}</span>
                      </li>
                      <li class="select-title-li">
                        模板功能：<span>{{ selectedtemplate.function.name }}</span>
                      </li>
                      <li class="select-title-li">
                        <i
                          class="el-icon-delete-solid"
                          style="color:red"
                          title="删除选中用户"
                          @click="selectedtemplate = {}"
                        />
                      </li>
                    </ul>

                    <div v-else style="display:inline-block;color: rgb(192,196,204); margin-top: 10px">
                      <i style="color: red" class="el-icon-error select-title-li" /> 没用选中任何模板~
                    </div>
                  </div>
                </template>
                <div v-show="JSON.stringify(selectedtemplate) !== '{}'">
                  <el-form label-position="left" size="mini">
                    <el-form-item label="模板名称:">
                      <div>{{ selectedtemplate.name }}</div>
                    </el-form-item>
                    <el-form-item label="支持设备:">
                      <span
                        v-for="(item , key) in selectedtemplate.support"
                        :key="key"
                        class="support-item"
                      >{{ item }}</span>
                    </el-form-item>

                    <el-form-item label="模板功能:">
                      <div>{{ selectedtemplate.function ? selectedtemplate.function.name : 'null' }}
                      </div>
                    </el-form-item>
                    <el-form-item label="模板描述:">
                      <div>{{ selectedtemplate.remark }}</div>
                    </el-form-item>
                    <el-form-item label="模板参数:">
                      <el-row>
                        <el-col v-for="(item, key) in selectedtemplate.params_set" :key="key" :span="24">
                          <span class="show-param—item">参数{{ key + 1 }}：{{ item.name }}</span>
                          <span class="show-param—item">描述：{{ item.remark }}</span>
                          <span class="show-param—item">约束：{{ item.constraint }}</span>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-form>
                  <h4>模板内容：</h4>
                  <template-edit class="code-block" :template="selectedtemplate" :read-only="true" />
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-col>
        </el-row>
      </div>
      <div v-else class="diy-content">
        <p>
          <label><span class="key">配置目标：</span>
            <el-radio-group v-model="action.source" size="mini">
              <el-radio-button label="running" />
<!--              <el-radio-button label="startup" />-->
<!--              <el-radio-button label="other" />-->
            </el-radio-group>
          </label>
        </p>
        <el-button-group>
          <el-button size="mini" type="primary" @click="handleSave">保存</el-button>
        </el-button-group>
        <codemirror v-model="resCodeData" :options="CmOptions" />
      </div>
    </div>
  </div>
</template>

<script>
import { getTemplatesList } from '@/api/configManage/templates'
import { parseTime } from '@/utils'
import TemplateEdit from '@/views/templateManage/templates/edit/index'

export default {
  name: 'ChioceTtempalte',
  components: { TemplateEdit },
  data() {
    return {
      selectedtemplate: {},
      listLoading: false,
      list: [],
      listQuery: {
        name: '',
        temptype: ''
      },
      configMode: '系统模板',
      configData: {},
      CmOptions: {
        mode: 'text/xml',
        tabSize: 4,
        theme: 'cobalt',
        lineNumbers: true,
        line: true,
        readOnly: false
      },
      action: {
        name: 'edit-config',
        TemType: 'merge',
        source: 'running'
      },
      resCodeData: ''
    }
  },
  created() {
    // this.getList()
  },
  methods: {
    handleCurrentChange(curr, old) {
      this.selectedtemplate = curr
      this.$emit('selectedtemplate', { selectedtemplate: this.selectedtemplate, configMode: this.configMode })
    },
    parseTime(time, format) {
      return parseTime(time, format)
    },
    handleFilter() {
      this.listLoading = true
      this.getList()
    },
    getList() {
      this.listLoading = true
      getTemplatesList(this.listQuery).then(response => {
        // console.log(response)
        if (response.results !== undefined) {
          this.list = response.results
        } else {
          this.list = response
        }
        this.listLoading = false
      }).catch(_ => {
        this.$message({ type: 'error', message: '获取模板列表失败。' })
      })
    },
    handleSave() {
      this.$emit('diyconfig', {
        resCodeData: this.resCodeData,
        configMode: this.configMode,
        action: this.action
      })
    }
  }
}
</script>

<style scoped>
.content {
  /*padding: 50px;*/
  margin-top: 20px;
  position: relative;
}

.left {
  text-align: center;
  padding: 0 20px;
}

.right {
  /*overflow-y: scroll;*/
  padding: 0 20px;
}

.support-item {
  margin-right: 10px;
}

.select-title-ul, .select-title-li {
  list-style: none;
  margin: 0;
  padding: 0;
}

.select-title-li {
  display: inline-block;
  margin-right: 10px;
}
.diy-content {
  padding: 20px;
}
</style>
