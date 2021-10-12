export const commonNetworkMixin = {
  data() {
    return {
      dialogEditShow: false,
      loadingInit: false
    }
  },
  methods: {
    opsSuccess(ops, fun) {
      // ops: string ，操作名称字符串; fun: 回调操作
      this.$message({ type: 'success', message: ops + '成功。' })
      this.getList()
      this.dialogEditShow = false
      this.loadingInit = false
      if (fun) fun()
    },
    opsError(error, ops, fun) {
      // ops: string ，操作名称字符串
      if (((error.response || {}).data || {}).msg) {
        const data = error.response['data']
        this.$message({ type: 'error', message: ops + '失败! ' + data['msg'] })
      } else {
        this.$message({ type: 'error', message: ops + '失败! ' })
      }
      this.loadingInit = false
      if (fun) fun()
    },
    getListError(error) {
      // console.log(error)
      if (((error.response || {}).data || {}).msg) {
        const data = error.response['data']
        this.$message({ type: 'error', message: data['msg'] })
      } else {
        this.$message({ type: 'error', message: ' 请求失败，请尝试刷新!' })
      }
      this.loadingInit = false
    }
  }
}
