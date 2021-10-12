import { fetchEquipmentList } from '@/api/equipment'

export const commonPagination = {
  data() {
    return {
      total: 0,
      listQuery: {
        page: 1,
        limit: 10,
        ip: undefined,
        name: undefined,
        type: undefined,
        sort: '+id'
      }
    }
  },
  methods: {
    getList() {
      // this.loadingInit = true
      // fetchEquipmentList(this.listQuery).then(response => {
      //   if (response !== null) {
      //     this.list = response.results
      //     this.total = response.count
      //   } else {
      //     this.list = []
      //     this.total = 0
      //   }
      //   this.loadingInit = false
      // }).catch(error => {
      //   console.log(error)
      //   this.$message({ type: 'error', message: '请求失败！' })
      // })
    }
  }
}
