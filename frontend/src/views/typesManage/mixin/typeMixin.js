import { commonPagination } from '@/views/mixins/commonPagination'
import Pagination from '@/components/Pagination/index'
export const typeMixin = {
  components: { Pagination },
  data() {
    return {
      loading: false,
      list: [],
      temp: {},
      flags: {
        addDialogVisible: false
      }
    }
  },
  methods: {
    updateType(getterName) {
      this.loading = true
      this.$store.dispatch('getTypes').then(res => {
        // enableEdit
        this.loading = false
        this.list = this.$store.getters[getterName].map(item => {
          const newItem = Object.assign({}, item)
          newItem.enableEdit = false
          return newItem
        })
      }).catch(erro => {
        this.loading = false
        console.log(erro)
      })
    }
  }
}
