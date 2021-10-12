/**
 * 对于dom操作的方法
 * **/
export const commonOperationMixin = {
  data() {
    return {
      dialogEditShow: false,
      loadingInit: false,
      dialogEditStatus: '',
      temp: {},
      dialogStatus: '',
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: 'Edit',
        create: 'Create'
      }
    }
  },
  methods: {
    // 关闭对话框
    beforeDialogClose(done) {
      // 传递一个函数名, 在点击确定后关闭
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {
        })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    handleCreate() {
      this.dialogEditStatus = 'create'
      this.dialogEditShow = true
    },
    createData() {
      alert('请重写createData()方法')
    },
    updateData() {
      alert('updateData()方法')
    }
  }
}
