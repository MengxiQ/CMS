<template>
  <ul class="my-menu">
    <slot></slot>
  </ul>
</template>

<script>
export default {
  name: 'MyMenu'
}
</script>

<style scoped>
 ul,i{
   margin: 0;
   padding: 0;
   list-style: none;
 }
</style>
