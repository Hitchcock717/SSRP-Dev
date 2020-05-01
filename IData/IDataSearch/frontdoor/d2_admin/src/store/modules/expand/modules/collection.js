import collectionService from '@api/demo/collection/collectionService'

const state = {
  collection: []
}

const getters = {
  collection: state => {
    return state.collection
  }
}

const actions = {
  getCollection ({ commit }) {
    collectionService.fetchCollection()
      .then(collection => {
        commit('setcollection', collection)
      })
  },
  deleteCollection ({ commit }, scope) {
    collectionService.deleteCollection(scope)
    commit('deletecollection', scope)
  }
}

const mutations = {
  setcollection (state, collection) {
    state.collection = collection
  },
  deletecollection (state, scope) {
    state.collection.splice(scope.$index, 1)
    state.collection = state.collection.filter(obj => obj.pk !== scope.row.pk)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
