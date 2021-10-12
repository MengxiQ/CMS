import { isArray } from '@/utils/isType'

export const baseMixinProps = {
  props: {
    ip: {
      type: String
    },
    list: {
      type: Array
    },
    params: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {
      dialogEditStatus: '',
      dialogEditShow: false,
      temp: {},
      loadingInit: false,
      listQuery: {
        page: 1,
        limit: 5,
        type: this.type,
        sort: '+id'
      },
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: '编辑',
        create: '创建'
      }
    }
  },
  methods: {
    isArray(o) {
      return isArray(o)
    },
    constraint(val) {
      return val.match('CHIOCE<(?<p>.*)>').groups.p.split(',')
    },
    beforCloseDialog() {
      this.dialogEditShow = false
      this.temp = {}
    },
    handleCreate() {
      this.dialogEditStatus = 'create'
      this.dialogEditShow = true
    },
    createSuccess() {
      this.$message({ type: 'success', message: '配置成功。' })
      this.dialogEditShow = false
      this.loadingInit = false
      this.$emit('createsuccess')
    },
    createError(error) {
      const data = error.response['data']
      this.$message({ type: 'error', message: ' 配置失败!   error:' + data['msg'] })
      this.loadingInit = false
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    getListError(error) {
      const data = error.response['data']
      this.$message({ type: 'error', message: ' 请求失败，请尝试刷新!' + data['msg'] })
      this.loadingInit = false
    }
  }

}
