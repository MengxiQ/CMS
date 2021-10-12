<template>
  <el-container>
    <el-aside class="aside" :width="asideWidth">
      <div class="fold-tool">
        <span v-show="isCollapse" class="el-icon-s-unfold" @click="unfold" />
        <span v-show="!isCollapse" class="el-icon-s-fold" @click="fold" />
      </div>
      <el-menu unique-opened default-active="" class="el-menu-vertical-demo" :collapse="isCollapse" @open="handleOpen" @close="handleClose" @select="select">
        <el-submenu index="vlan">
          <template slot="title">
            <i class="el-icon-s-management" />
            <span>VLAN管理</span>
          </template>
          <el-menu-item index="list">VLAN列表</el-menu-item>
        </el-submenu>
        <el-submenu index="interface">
          <template slot="title">
            <i class="el-icon-s-management" />
            <span>接口管理</span>
          </template>
          <el-menu-item index="monitoring">接口监控</el-menu-item>
          <el-menu-item index="common">通用接口</el-menu-item>
          <el-menu-item index="ethernet">以太接口</el-menu-item>
          <el-menu-item index="eth-trunk">Eth-Trunk</el-menu-item>
        </el-submenu>
        <el-submenu index="route">
          <template slot="title">
            <i class="el-icon-s-management" />
            <span>IP路由</span>
          </template>
          <el-menu-item index="table">路由表</el-menu-item>
          <el-menu-item index="ospf">OSPF协议</el-menu-item>
          <el-menu-item index="bgp">BGP协议</el-menu-item>
          <el-menu-item index="static">静态路由</el-menu-item>
        </el-submenu>
        <el-submenu index="manage">
          <template slot="title">
            <i class="el-icon-s-management" />
            <span>配置管理</span>
          </template>
          <el-menu-item index="setting">配置设置</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>
    <el-main class="main">
      <keep-alive><router-view/></keep-alive>
    </el-main>
  </el-container>
</template>

<script>
import { detailMixins } from '@/views/equipmentsManage/detail/components/minxins/detailMixins'
export default {
  name: 'Configuration',
  mixins: [detailMixins],
  data() {
    return {
      activeName: 'vlans'
    }
  },
  methods: {
    select(key, keyPath) {
      // console.log(key, keyPath)
      const basePath = '/equipmentsManage/detail/' + this.$route.params.ip + '/configuration/'
      // console.log(basePath + keyPath[0] + '/' + keyPath[1])
      if (keyPath[2]) {
        console.log(basePath + keyPath[0] + '/' + keyPath[1] + '/' + keyPath[2])
        this.$router.push({ path: basePath + keyPath[0] + '/' + keyPath[1] + '/' + keyPath[2] })
      } else {
        this.$router.push({ path: basePath + keyPath[0] + '/' + keyPath[1] })
      }
    }
  }
}
</script>

<style scoped>
  .inner-sub-item-title {
    width: 100%; display: inline-block; text-align: center;
  }
  /*.submenu {*/
  /*  margin-right: 10px;text-align: left*/
  /*}*/
</style>
<style>
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
.el-menu-vertical-demo:not(.el-menu--collapse) {
  /*width: 150px;*/
  /*overflow-y: scroll;*/
  overflow-x: hidden;
}
.el-submenu__icon-arrow {
     display: block !important;
}
.el-menu--vertical .nest-menu .el-submenu > .el-submenu__title:hover, .el-menu--vertical .el-menu-item:hover{
    background-color: #ecf5ff !important;
}
.aside {
  transition: width 0.1s;
}
</style>
