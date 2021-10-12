export const monitoringMixin = {
  props: {
    ip: {
      type: String
    }
  },
  data() {
    return {
      list: [],
      loadingInit: true
    }
  },
  methods: {
    getListError(error) {
      if (error.response) {
        const data = error.response['data']
        this.$message({ type: 'error', message: ' 请求失败，正在尝试重新刷新!   error:' + data['msg'] })
      } else {
        console.log(error)
        // this.$message({ type: 'error', message: ' 请求失败，正在尝试重新刷新!' })
      }
      this.loadingInit = false
      // this.timer = setTimeout(_ => {
      //   console.log('try again!')
      //   this.getList()
      // }, 5000)
    }
  },
  mounted() {
    this.getList()
  }
}
