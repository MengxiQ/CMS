<template>
  <el-button-group class="heard-tool">
    <el-button size="mini" type="primary" icon="el-icon-edit" @click="add">添加</el-button>
    <el-button size="mini" type="success" @click="refresh">刷新</el-button>
    <slot/>
  </el-button-group>
</template>

<script>
export default {
  name: 'ButtonGroup',
  methods: {
    add() {
      this.$emit('add')
    },
    refresh() {
      this.$emit('refresh')
    }
  }
}
</script>

<style scoped>
  .heard-tool {
    /*padding: 10px;*/
  }
</style>
