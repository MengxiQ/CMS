<template>
    <el-aside class="aside" :width="asideWidth">
      <el-button-group style="position: absolute; z-index: 1000; left: 0; top: 65px">
        <el-button v-show="isCollapse" size="mini" icon="el-icon-s-unfold" @click="unfold" />
        <el-button v-show="!isCollapse" size="mini" icon="el-icon-s-fold" @click="fold" />
      </el-button-group>
      <el-menu router default-active="base" class="el-menu-vertical-demo" :collapse="isCollapse" @open="handleOpen" @close="handleClose">
        <!--        <el-submenu index="1">-->
        <!--          <template slot="title">-->
        <!--            <i class="el-icon-location" />-->
        <!--            <span>导航一</span>-->
        <!--          </template>-->
        <!--          <el-menu-item-group>-->
        <!--            <template slot="title">分组一</template>-->
        <!--            <el-menu-item index="1-1">选项1</el-menu-item>-->
        <!--            <el-menu-item index="1-2">选项2</el-menu-item>-->
        <!--          </el-menu-item-group>-->
        <!--          <el-menu-item-group title="分组2">-->
        <!--            <el-menu-item index="1-3">选项3</el-menu-item>-->
        <!--          </el-menu-item-group>-->
        <!--        </el-submenu>-->
        <el-menu-item index="base">
          <i class="el-icon-menu" />
          <span slot="title">基本信息</span>
        </el-menu-item>
        <el-menu-item index="3">
          <i class="el-icon-document" />
          <span slot="title">告警信息</span>
        </el-menu-item>
        <el-menu-item index="4">
          <i class="el-icon-setting" />
          <span slot="title">日志信息</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
</template>
<script>
export default {
  name: 'Aside'
}
</script>

<style scoped>

</style>
<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 150px;
}
.el-submenu__icon-arrow {
     display: inline-block !important;
}
.el-menu--vertical .nest-menu .el-submenu > .el-submenu__title:hover, .el-menu--vertical .el-menu-item:hover{
    background-color: #ecf5ff !important;
}
.aside {
  transition: width 0.4s;
}
</style>

