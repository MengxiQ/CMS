<template>
  <div class="content">
    <el-row>
      <el-col :md="9" :lg="8">
        <div class="content-form">
          <h5 style="border-left: 4px solid rgb(0,34,64); padding:0px 10px">名称：{{ template.name }}</h5>
          <p style="font-size: smaller;padding: 0 5px 5px 5px">功能：{{ template.function ? template.function.name : '' }}</p>
          <el-form label-position="" label-width="100px">
            <el-form-item
              v-for="(item, key) in template.params_set"
              :key="key"
              style="position: relative; padding: 10px 0 20px 0"
              :label="item.name"
              size="medium"
            >
              <div style="position: absolute;z-index: 100;top: -28px; font-size: smaller; color: #5a5e66">{{ item.remark }}
                <span style="margin-left: 5px;color: #3d7ed5">({{ item.constraint }})</span></div>
              <el-select
                v-if="(item.constraint).match('CHIOCE<(?<p>.*)>')"
                v-model="temp[item.name]"
              >
                <el-option
                  v-for="(i, k) in constraint(item.constraint)"
                  :key="k"
                  :value="i"
                  :label="i"
                />
              </el-select>
              <el-switch
                v-if="item.constraint === 'BLOOEAN'"
                v-model="temp[item.name]"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-value="true"
                inactive-value="false"
              />
              <el-input
                v-if="item.constraint.search('INT') >= 0 || item.constraint === 'IP' || item.constraint === 'MASK' || item.constraint === 'WILDCARD' || item.constraint.search('STRING') >= 0"
                v-model="temp[item.name]"
              />
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col :md="15" :lg="16">
        <div content="content-generate">
          <p>
            <label><span class="key">模板类型：</span>
              <el-radio-group v-model="action.TemType" size="mini">
                <el-radio-button label="merge" />
                <el-radio-button label="delete" />
              </el-radio-group>
            </label>
          </p>
          <p>
            <label><span class="key">配置源：</span>
              <el-radio-group v-model="action.source" size="mini">
                <el-radio-button label="running" />
                <!--                <el-radio-button label="startup"></el-radio-button>-->
                <!--                <el-radio-button label="other"></el-radio-button>-->
              </el-radio-group>
            </label>
          </p>
          <el-button-group>
            <el-button size="mini" type="primary" :disabled="loading" @click="handleGenerate"><i v-if="loading" class="el-icon-loading" />生成配置</el-button>
            <el-button size="mini" type="primary" @click="handleSave">保存</el-button>
          </el-button-group>
          <codemirror v-model="resCodeData" :options="CmOptions" />
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import 'codemirror/mode/xml/xml' // 必须提前引入，因为vue 貌似没有无法在实例初始化后再动态加载对应
import 'codemirror/theme/cobalt.css'
import { GenerateConfig } from '@/api/configManage/tools'
import { isArray } from '@/utils/validate'

export default {
  name: 'ConfigTemplate',
  props: {
    template: {
      type: Object
    },
    configmode: {
      type: String
    }
  },
  data() {
    return {
      loading: false,
      temp: {},
      configData: {},
      CmOptions: {
        mode: 'text/xml',
        tabSize: 4,
        theme: 'cobalt',
        lineNumbers: true,
        line: true,
        readOnly: false
      },
      resCodeData: '',
      action: {
        name: 'edit-config',
        TemType: 'merge',
        source: 'running'
      }
    }
  },
  watch: {
    template(value) {
      // 默认没有填写的输入框是没有在temp中生成属性，而后端解析模板需要所有的属性列表，所以赋值所有默认为空字符串
      this.$nextTick(_ => {
        const temp = {}
        if (isArray(value.params_set)) {
          value.params_set.map(item => {
            temp[item.name] = ''
          })
        }
        this.temp = temp
      })
    }
  },
  methods: {
    constraint(val) {
      return val.match('CHIOCE<(?<p>.*)>').groups.p.split(',')
    },
    handleGenerate() {
      // console.log(this.template.templateData)
      const data = {
        temp: this.temp,
        template: this.template.templateData,
        configMode: this.configmode,
        action: this.action
      }
      this.loading = true
      GenerateConfig(data).then(res => {
        this.resCodeData = res.data
        this.loading = false
      }).catch(error => {
        console.log(error)
        this.loading = false
        this.$message({ type: 'error', message: '生成模板失败。' })
      })
    },
    handleSave() {
      this.$emit('generateconfig', {
        resCodeData: this.resCodeData,
        configMode: this.configmode,
        action: this.action
      })
    }
  }
}
</script>

<style scoped>
.content {
  padding: 10px;
}

.content-form {
  /*width: 500px;*/
  padding: 15px;
}

.key {
  font-size: smaller;
}
</style>
