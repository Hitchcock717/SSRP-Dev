import extractorService from '@api/demo/extractorService'

const state = {
  extractors: []
}

const getters = {
  extractors: state => {
    return state.extractors
  }
}

const actions = {
  getExtractors ({ commit }) {
    extractorService.fetchExtractors()
      .then(extractors => {
        commit('setextractors', extractors)
      })
  },
  deleteExtractor ({ commit }, extrId) {
    extractorService.deleteextractor(extrId)
    commit('deleteextractor', extrId)
  }
}

const mutations = {
  setextractors (state, extractors) {
    state.extractors = extractors
  },
  deleteextractor (state, extrId) {
    state.extractors = state.extractors.filter(obj => obj.pk !== extrId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
