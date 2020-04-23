import filterResultService from '@api/demo/filterResultService'

const state = {
  filterResult: []
}

const getters = {
  filterResult: state => {
    return state.filterResult
  }
}

const actions = {
  getfilterResult ({ commit }) {
    filterResultService.fetchfilterResult()
      .then(filterResult => {
        commit('setfilterResult', filterResult)
      })
  }
}

const mutations = {
  setfilterResult (state, filterResult) {
    state.filterResult = filterResult
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
