export const detailMixins = {
  data() {
    return {
      isCollapse: false,
      asideWidth: '150px'
    }
  },
  computed: {
    ip() {
      return this.$route.params.ip
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      // console.log(key, keyPath)
    },
    handleClose(key, keyPath) {
      // console.log(key, keyPath)
    },
    // select(key, keyPath) {
    //   // console.log(key, keyPath)
    //   const basePath = '/equipmentsManage/detail/' + this.$route.params.ip + '/configuration/'
    //   // console.log(basePath + keyPath[0] + '/' + keyPath[1])
    //   if (keyPath[2]) {
    //     console.log(basePath + keyPath[0] + '/' + keyPath[1] + '/' + keyPath[2])
    //     this.$router.push({ path: basePath + keyPath[0] + '/' + keyPath[1] + '/' + keyPath[2] })
    //   } else {
    //     this.$router.push({ path: basePath + keyPath[0] + '/' + keyPath[1] })
    //   }
    // },
    fold() {
      this.asideWidth = '65px'
      this.isCollapse = true
    },
    unfold() {
      this.asideWidth = '150px'
      this.isCollapse = false
    }
  }
}
