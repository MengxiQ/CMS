<template>
  <div>
    <el-table-column v-for="(item, key) in params" v-if="item.role !== 'key'" :key="key" :label="item.label" :prop="item.name" />
  </div>
</template>

<script>
export default {
  name: 'ConfigTable',
  props: {
    params: {
      type: Array,
      default() { return [] }
    }
  }
}
</script>

<style scoped>

</style>
