import recommendService from '@api/demo/recommendService'

const state = {
  recommends: []
}

const getters = {
  recommends: state => {
    return state.recommends
  }
}

const actions = {
  getRecommends ({ commit }) {
    recommendService.fetchRecommends()
      .then(recommends => {
        commit('setrecommends', recommends)
        commit('saverecommends', recommends)
      })
  },
  deleteRecommend ({ commit }, recomId) {
    recommendService.deleteRecommend(recomId)
    commit('deleterecommend', recomId)
  }
}

const mutations = {
  setrecommends (state, recommends) {
    state.recommends = recommends
  },
  saverecommends (state, recommends) {
    const parsed = JSON.stringify(recommends)
    localStorage.setItem('recommends', parsed)
  },
  deleterecommend (state, recomId) {
    state.recommends = state.recommends.filter(obj => obj.pk !== recomId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
