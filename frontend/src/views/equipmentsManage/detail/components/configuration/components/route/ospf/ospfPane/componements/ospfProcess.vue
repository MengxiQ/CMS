<template>
  <div class="content">
    <el-row>
      <el-col :span="12" class="col">
        <span class="title">进程ID</span>
        <span class="form-titem-valus">{{ item.processId }}</span></el-col>
      <el-col :span="12" class="col">
        <span class="title">路由ID</span>
        <span class="form-titem-valus">{{ item.routerId === null ? 'NULL' : item.routerId }}</span></el-col>
      <el-col :span="12" class="col">
        <span class="title">描述</span>
        <span class="form-titem-valus">{{ item.description === null ? 'NULL' : item.description }}</span></el-col>
      <el-col :span="12" class="col">
        <span class="title">vrfName</span>
        <span class="form-titem-valus">{{ item.vrfName }}</span></el-col>
    </el-row>
  </div>
</template>

<script>

export default {
  name: 'OspfProcess',
  props: {
    item: {
      type: Object
    },
    ip: {
      type: String
    }
  },
  data() {
    return {
      params: []
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.col {
  padding: 10px;
}
.content {
  font-size: smaller;
}
.title {
  color: #6f7180;
  margin-right: 10px;
}
.form-titem-valus {
  margin-right: 20px;

}
</style>
