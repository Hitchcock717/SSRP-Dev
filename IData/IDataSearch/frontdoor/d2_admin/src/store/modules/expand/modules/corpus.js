import corpusService from '@api/demo/corpus/corpusService'

const state = {
  corpus: []
}

const getters = {
  corpus: state => {
    return state.corpus
  }
}

const actions = {
  getCorpus ({ commit }, selectedCorpus) {
    corpusService.postCorpus(selectedCorpus)
      .then(res => {
        commit('fetchcorpus', res)
      })
  },
  deleteCorpus ({ commit }, scope) {
    corpusService.deleteCorpus(scope)
    commit('deletecorpus', scope)
  }
}

const mutations = {
  fetchcorpus (state, res) {
    this.result = res
    if (this.result === 'failed') {
      alert('该词表为空,请添加词汇!')
    } else {
      state.corpus = this.result
    }
  },
  deletecorpus (state, scope) {
    console.log(scope.$index)
    state.corpus.splice(scope.$index, 1)
    state.corpus = state.corpus.filter(obj => obj.pk !== scope.row.pk)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
