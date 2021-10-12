import { getTemplateTypesList, getUnitTypesList, getFunctionsList, getNeTypesList, getVendorTypesList} from '@/api/typesManage'

const state = {
  templateTypes: [],
  unitTypes: [],
  functionTypes: [],
  neTypes: [],
  vendorTypes: []
}

const mutations = {
  addTemplateType(state, data) {
    state.templateTypes.push(data)
  },
  deleteTemplateType(state, key) {
    state.toposData.splice(key, 1)
  },
  updateTemplateType(state, data) {
    state.templateTypes[data.key] = data
  },
  getTemplateTypes(state, data) {
    state.templateTypes = data
  },
  getUnitTypes(state, data) {
    state.unitTypes = data
  },
  getFunctions(state, data) {
    state.functionTypes = data
  },
  getNeTypes(state, data) {
    state.neTypes = data
  },
  getVendorTypes(state, data) {
    state.vendorTypes = data
  }
}

const actions = {
  getTypes(context) {
    const promiseArr = [
      getTemplateTypesList().then(res => {
        context.commit('getTemplateTypes', res)
      }).catch(),
      getUnitTypesList().then(res => {
        context.commit('getUnitTypes', res)
      }).catch(),
      getFunctionsList().then(res => {
        context.commit('getFunctions', res)
      }).catch(),
      getNeTypesList().then(res => {
        context.commit('getNeTypes', res)
      }).catch(),
      getVendorTypesList().then(res => {
        context.commit('getVendorTypes', res)
      }).catch()
    ]
    return Promise.all(promiseArr)
  }

}

export default {
  namespace: true,
  state,
  mutations,
  actions
}
