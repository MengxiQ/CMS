<template>
  <div>
    <codemirror v-model="template.templateData" :options="cmOptions" />
  </div>
</template>

<script>
// import 'codemirror/mode/javascript/javascript.js' // 必须提前引入，因为vue 貌似没有无法在实例初始化后再动态加载对应 J
import 'codemirror/mode/xml/xml' // 必须提前引入，因为vue 貌似没有无法在实例初始化后再动态加载对应
import 'codemirror/theme/cobalt.css'
export default {
  name: 'TemplateEdit',
  props: {
    template: {},
    readOnly: {
      default() {
        return false
      }
    }
  },
  data() {
    return {
      cmOptions: {
        // tabSize: 4,
        mode: 'text/xml',
        tabSize: 4,
        // mode: 'text/javascript',
        // theme: 'base16-dark',
        // theme: 'cobalt',
        lineNumbers: true,
        line: true,
        readOnly: this.readOnly
      }
    }
  }
}
</script>

<style scoped>

</style>
