export const props = {
  props: {
    editable: {
      type: Boolean,
      default: true
    },
    topoData: {
      type: Object,
      default() {
        return {}
      },
      required: true
    },
    TopoTitle: {
      type: String,
      default() {
        return '新建Topo视图'
      }
    }
  }
}
