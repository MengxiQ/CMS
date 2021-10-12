import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import types from '@/store/modules/types'
import config from '@/store/modules/config'
import permission from '@/store/modules/permission'
import tagsView from '@/store/modules/tagsView'
Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    types,
    config,
    permission,
    tagsView
  },
  getters
})

export default store
