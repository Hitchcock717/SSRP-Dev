import rawResultService from '@api/demo/rawResultService'

const state = {
  rawResult: []
}

const getters = {
  rawResult: state => {
    return state.rawResult
  }
}

const actions = {
  getrawResult ({ commit }) {
    rawResultService.fetchrawResult()
      .then(rawResult => {
        commit('setrawResult', rawResult)
      })
  }
}

const mutations = {
  setrawResult (state, rawResult) {
    state.rawResult = rawResult
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
