import { isArray } from '@/utils/isType'

export const viewBaseMinxin = {
  props: {
  },
  data() {
    return {
      toppsList: [],
      dialogEditStatus: '',
      dialogEditShow: false,
      loadingInit: true,
      temp: {},
      listQuery: {
        page: 1,
        limit: 5,
        type: this.type,
        sort: '+id'
      }
    }
  },
  methods: {
    isArray(o) {
      return isArray(o)
    },
    beforCloseDialog() {
      this.dialogEditShow = false
      this.temp = {}
    },
    handleCreate() {
      this.dialogEditStatus = 'create'
      this.dialogEditShow = true
    },
    opsSuccess(ops) {
      this.$message({ type: 'success', message: ops + '成功。' })
      this.getList()
      this.dialogEditShow = false
      this.loadingInit = false
    },
    opsError(error, ops) {
      const data = error.response['data']
      this.$message({ type: 'error', message: ops + ' 失败!   error:' + data['msg'] })
      this.loadingInit = false
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    getListError(error) {
      if (error.response) {
        const data = error.response['data']
        this.$message({ type: 'error', message: ' 请求失败，请尝试刷新!   error:' + data['msg'] })
      } else {
        console.log(error)
        // this.$message({ type: 'error', message: ' 请求失败，尝试刷新!' })
      }
      this.loadingInit = false
    }
  },
  mounted() {
    this.getList()
  }
}
