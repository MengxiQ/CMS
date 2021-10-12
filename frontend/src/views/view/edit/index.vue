<template>
  <div class="edit">
    <!-- 输入新建信息-->
    <div v-if="!isCanEdit" class="desc-content" >
      <img class="main-iron" src="@/assets/bg/zs_icon_xscl.svg">
      <p class="desc">
        创建拓扑可以方便配置和管理网络，点击按钮开始创建topo。
        <el-button size="mini" type="primary" @click="isShowEditDailog = true">新建视图</el-button></p>

    </div>
    <div v-else class="topoArea">
      <!--      编辑拓扑-->
      <v-topo :eidtable="true" :topoData="topoData" @savesuccess="saveSuccess"></v-topo>
    </div>
    <el-dialog
      title="新建topo视图"
      :visible.sync="isShowEditDailog"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="left">
        <el-form-item label="名称" label-width="50px">
          <el-input size="" v-model="topoData.name" placeholder="请输入新建topo名称"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" @click="isShowEditDailog = false">取 消</el-button>
        <el-button size="mini" type="primary" @click="isShowEditDailog = false;isCanEdit=true">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import VTopo from '@/components/vuetopo/vTopo/vTopo'
export default {
  name: 'Index',
  components: { VTopo },
  data: function() {
    return {
      isCanEdit: false,
      isShowEditDailog: true,
      topoData: {
        'name': '',
        'nodes': [],
        'connectors': []
      }
    }
  },
  methods: {
    // 关闭对话框
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {
        })
    },
    saveSuccess() {
      // 保存成功
      // 清空
      this.topoData = {
        'name': '',
        'nodes': [],
        'connectors': []
      }
      this.isCanEdit = false
    }
  }
}
</script>

<style lang="less" scoped>
.edit{
  height: 100vh;
  width: 100%;
}
body{background:url('/src/assets/topo/canvas_bg.jpg');}
#app{height:100%}
 .topoArea{height:calc(~"100% - 70px");min-height: 800px;box-sizing: border-box;}

 .main-iron{
   height: 200px;
   width: 200px;
   margin: auto;
   display: block;
 }
 .desc{
   width: 500px;
   display: block;
   margin: auto;
   line-height: 25px;
   text-align: center;
 }
 .desc-content {
   margin-top: 100px;
 }
</style>
