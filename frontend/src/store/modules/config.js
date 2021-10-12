const state = {
  source: 'running'
}

const mutations = {
  settingSource(state, data) {
    state.source = data
  }
}

export default {
  namespace: true,
  state,
  mutations
  // actions
}
