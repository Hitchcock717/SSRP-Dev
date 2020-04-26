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
        commit('saverawResult', rawResult)
        alert('数据加载成功!')
      })
  }
}

const mutations = {
  setrawResult (state, rawResult) {
    state.rawResult = rawResult
  },
  saverawResult (state, rawResult) {
    const parsed = JSON.stringify(rawResult)
    localStorage.setItem('rawResult', parsed)
    // console.log(parsed)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
