import { commonOperationMixin } from '@/views/mixins/commonOperationMixin'
import { commonNetworkMixin } from '@/views/mixins/commonNetwork'
import { commonValidateMixin } from '@/views/mixins/commonValidateMixin'

export const baseMinxin = {
  mixins: [commonNetworkMixin, commonOperationMixin, commonValidateMixin],
  computed: {
    ip() {
      return this.$route.params.ip
    }
  },
  data() {
    return {
      dataSource: '', // 标识当前的数据是那个数据库的
      list: [],
      dialogEditStatus: '',
      dialogEditShow: false,
      params: [],
      temp: {},
      loadingInit: true,
      textMap: { // 重写这个以达到显示创建和编辑框的显示标题
        update: '编辑',
        create: '创建'
      }
    }
  },
  methods: {
    constraint(val) {
      return val.match('CHIOCE<(?<p>.*)>').groups.p.split(',')
    },
    defaultTemp() {
      // 不要计算属性，因为缓存不需要动态改变
      // 确定给edit组件传什么默认值
      if (this.dialogEditStatus === 'update') {
        return this.temp
      } else return {}
    },
    disparams() {
      // // 不要计算属性，因为缓存不需要动态改变
      // if (this.dialogEditStatus === 'update') {
      //   // 如果为编辑模式，则下列字段为不可修改
      //   return ['prefix', 'maskLength', 'ifName', 'nexthop']
      // } else return []
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
      this.getList()
      this.dialogEditShow = false
      this.loadingInit = false
    },
    deleteSuccess() {
      this.$message({ type: 'success', message: '配置成功。' })
      this.getList()
      this.dialogEditShow = false
      this.loadingInit = false
    },
    createError(error) {
      if (((error.response || {}).data || {}).msg) {
        const data = error.response['data']
        this.$message({ type: 'error', message: data['msg'] })
      } else {
        // 获取不到后台报错信息
        this.$message({ type: 'error', message: ' 创建失败.' })
      }
      this.loadingInit = false
    },
    deleteError(error) {
      if (((error.response || {}).data || {}).msg) {
        const data = error.response['data']
        this.$message({ type: 'error', message: data['msg'] })
      } else {
        // 获取不到后台报错信息
        this.$message({ type: 'error', message: ' 创建失败.' })
      }
      this.loadingInit = false
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogEditStatus = 'update'
      this.dialogEditShow = true
    },
    getList() {
      /** 重写该方法，模板： **/
      // begin
      // this.loadingInit = true
      // const query = {
      //   ip: this.ip,
      //   source: this.$store.getters.source
      // }
      // then()
    },
    getListError(error) {
      console.log(error)
      // console.log(error.response)
      // 尝试获取后台报错信息
      if (((error.response || {}).data || {}).msg) {
        const data = error.response.data
        // console.log(data.msg)
        if (data.msg.match('candidate data store does not exist.') !== null) {
          // 候选数据没有创建
          this.list = []
          this.dataSource = this.$store.getters.source
          this.$message({ type: 'info', message: '开始配置并创建candidate数据库.' })
        } else {
          this.$message({ type: 'error', message: data.msg })
        }
      } else {
        // 获取不到后台报错信息
        this.$message({ type: 'error', message: ' 请求失败，请尝试刷新.' })
      }
      // 关闭加载提示
      this.loadingInit = false
    },
    getListSuccess(res, query) {
      this.params = res.params
      this.dataSource = query.source
      this.loadingInit = false
    }
  },
  mounted() {
    this.getList()
  }
}
