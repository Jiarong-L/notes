import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state () {          
    return {
      ValA: 'ok'
    }
  },
  getters: {
    len () {console.log('Getters Computed'); return 10}
  },
  mutations: {
    func1 (state, inputVal) {state.ValA = inputVal}
  },
  actions: {
    delayfunc1 (store, inputVal) {
      setTimeout(()=>{store.commit('func1',inputVal)},3000)
    }
  },
  modules: {
    mA: {
      state: {},
      mutations: {},
      actions: {}
    },
    mB: {
      getters: {}
    }
  }
})
