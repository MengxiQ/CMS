<template>
  <el-container>
    <el-aside class="aside" :width="asideWidth">
      <div class="fold-tool">
        <span v-show="isCollapse" class="el-icon-s-unfold" @click="unfold" />
        <span v-show="!isCollapse" class="el-icon-s-fold" @click="fold" />
      </div>
      <el-menu router default-active="network" class="el-menu-vertical-demo" :collapse="isCollapse" @open="handleOpen" @close="handleClose">
        <el-menu-item index="network">
          <i class="el-icon-s-marketing" />
          <span slot="title">PING测试</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="page-content">
      <keep-alive>
        <router-view />
      </keep-alive>
    </el-main>
  </el-container>
</template>

<script>
import { detailMixins } from '@/views/equipmentsManage/detail/components/minxins/detailMixins'
export default {
  name: 'Test',
  mixins: [detailMixins]
}
</script>

<style scoped>
.fold-tool {
  position: absolute; z-index: 1000; left: 22px; top: 22px; transition: all 0.2s;
  /*background-color: red;*/
}
.fold-tool:hover {
  cursor: pointer;
  color: rgb(64,158,255);
}
.fold-tool>span {
  font-size: 22px;
}
</style>
