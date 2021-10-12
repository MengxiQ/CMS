<template>
  <span class="my-menu-item">
    <i class="el-icon-ice-cream-round"></i>
    <span class="my-menu-item-text"><slot></slot></span>
  </span>
</template>

<script>
export default {
  name: 'MyMenuItem',
  props: {
    index: {
      type: String
    }
  }
}
</script>

<style scoped>
 .my-menu-item {
   display: inline-block;
   padding: 5px;
   margin-right: 10px;
 }
 .my-menu-item:hover {
   cursor: pointer;
   color: red;
 }
</style>
