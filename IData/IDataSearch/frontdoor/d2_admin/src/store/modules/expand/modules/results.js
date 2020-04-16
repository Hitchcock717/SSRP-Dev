import resultService from '@api/demo/resultService'

const state = {
  result: ''
}

const getters = {
  result: state => {
    return state.result
  }
}

const actions = {
  getResult ({ commit }) {
    resultService.fetchResult()
      .then(result => {
        commit('setResult', result)
      })
  }
}

const mutations = {
  setResult (state, result) {
    state.result = result
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
