<template>
  <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
</template>

<script>
export default {
  name: 'Pagination'
}
</script>

<style scoped>

</style>
