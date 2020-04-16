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
        commit('saveextractors', extractors)
      })
  },
  deleteExtractor ({ commit }, extrId) {
    extractorService.deleteExtractor(extrId)
    commit('deleteextractor', extrId)
  }
}

const mutations = {
  setextractors (state, extractors) {
    state.extractors = extractors
  },
  saveextractors (state, extractors) {
    const parsed = JSON.stringify(extractors)
    localStorage.setItem('extractors', parsed)
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
