<template>
  <div>
    <el-radio-group title="选择显示表头的名称" v-model="showLabel" size="mini" style="transform: scale(0.9);position: absolute; top: 55px; left: 15px">
      <el-radio-button label="标签" />
      <el-radio-button label="名称" />
    </el-radio-group>
    <el-link
      type="primary"
      style="position: absolute; top: 55px; right: 20px"
      @click="temp = Object.assign({}, default_temp)"
    ><i class="el-icon-refresh-left">重置</i></el-link>
    <el-form v-model="temp" label-width="100px" style="padding-right: 20px">
      <el-form-item
        v-for="(item, key) in params"
        :key="key"
        :label="item[LabelMap[showLabel]]"
      >
        <!--        <div style="position: absolute;z-index: 100;top: -28px; font-size: smaller; color: #5a5e66">{{ item.remark }}-->
        <!--&lt;!&ndash;          <span style="margin-left: 5px;color: #3d7ed5">({{ item.constraint }})</span>&ndash;&gt;-->
        <!--        </div>-->
        <!--自动补全 提供默认选项-->
        <el-autocomplete
          v-if="item.constraint.match('DEFAULT<?(?<p>.*)>?')"
          v-model="temp[item.name]"
          :fetch-suggestions="querySearch"
          placeholder="请输入内容"
          :disabled="isDisable(item.name)"
        />
        <!--选项少的是时候使用radio-->
        <el-radio-group
          v-if="(item.constraint).match('CHIOCE<(?<p>.*)>') && constraint(item.constraint).length <= 4"
          v-model="temp[item.name]"
          size="mini"
        >
          <el-radio-button
            v-for="(i, k) in constraint(item.constraint)"
            :key="k"
            :label="i"
          />
        </el-radio-group>
        <!--选项多的时候使用select-->
        <el-select
          v-if="(item.constraint).match('CHIOCE<(?<p>.*)>') && constraint(item.constraint).length > 4"
          v-model="temp[item.name]"
          :disabled="isDisable(item.name)"
        >
          <el-option
            v-for="(i, k) in constraint(item.constraint)"
            :key="k"
            :value="i"
            :label="i"
          />
        </el-select>
        <el-switch
          v-if="item.constraint === 'BOOLEAN'"
          v-model="temp[item.name]"
          active-color="#13ce66"
          inactive-color="#ff4949"
          :active-value="'true'"
          :inactive-value="'false'"
          :disabled="isDisable(item.name)"
        />
        <el-input
          v-if="item.constraint.match('INT<?(?<p>.*)>?') || item.constraint === 'IP' || item.constraint === 'MASK' || item.constraint === 'WILDCARD' || item.constraint === 'STRING'"
          v-model="temp[item.name]"
          :disabled="isDisable(item.name)"
        />
        <el-popover
          placement="bottom"
          :title="item[LabelMap[showLabel]]"
          width="200"
          trigger="hover"
          :content="item.remark"
        >
          <i v-if="item.remark !== null && item.remark !== ''" slot="reference" class="el-icon-question question" />
        </el-popover>
      </el-form-item>
    </el-form>
    <el-row>
      <el-col :span="24" style="text-align: right">
        <el-button type="primary" @click="handleSave()">配置</el-button>
        <el-button type="" @click="handleCancel">取消</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Edit',
  props: {
    dialogEditShow: {
      type: Boolean,
      default() {
        return false
      }
    },
    params: {
      type: Array,
      default() {
        return []
      }
    },
    disparams: {
      // 默认的temp
      type: Array,
      default() { return [] }
    },
    default_temp: {
      type: Object,
      default() { return {} }
    }
  },
  data() {
    return {
      temp: {},
      showLabel: '标签',
      LabelMap: {
        '标签': 'label',
        '名称': 'name'
      }
    }
  },
  watch: {
    default_temp(n, o) {
      // 如果父组件更新default_temp，重新赋值表单
      this.temp = Object.assign({}, n)
    }
  },
  created() {
    this.temp = Object.assign({}, this.default_temp)
  },
  methods: {
    isDisable(name) {
      const result = this.disparams.filter(item => {
        return name === item
      })
      // 如果没有找到返回空数组[]
      if (JSON.stringify(result) !== '[]') {
        return true
      } else return false
    },
    constraint(val) {
      return val.match('CHIOCE<(?<p>.*)>').groups.p.split(',')
    },
    handleSave() {
      // 将最终的数据返回给父组件
      this.$emit('save', this.temp)
    },
    handleCancel() {
      // 取消
      // 清空表单
      this.temp = {}
      this.$emit('cancel')
    },
    querySearch(queryString, cb) {
      // cb 返回选项
      cb(this.createFilter())
    },
    createFilter() {
      // 生成默认选项
      this.Filter = []
      this.params.forEach(item => {
        const match = item.constraint.match('DEFAULT<?(?<p>.*)>')
        if (match !== null) {
          const value = match.groups.p
          this.Filter.push({ value: value })
        }
      })
      return this.Filter
    }
  }
}
</script>

<style scoped>
 .question {
   color: #34bfa3;
   position: absolute;
   top: 12px;
   right: -20px;
   font-size: larger;
 }
 .question:hover {
   cursor: pointer;
 }
</style>
