import repositoryService from '@api/demo/repository/repositoryService'

const state = {
  repositorys: []
}

const getters = {
  repositorys: state => {
    return state.repositorys
  }
}

const actions = {
  getRepositorys ({ commit }) {
    repositoryService.fetchRepository()
      .then(repositorys => {
        commit('setRepositorys', repositorys)
      })
  },
  deleteRepository ({ commit }, repoId) {
    repositoryService.deleteRepository(repoId)
    commit('deleteRepository', repoId)
  }
}

const mutations = {
  setRepositorys (state, repositorys) {
    state.repositorys = repositorys
  },
  deleteRepository (state, scope) {
    state.repositorys.splice(scope.$index, 1)
    state.repositorys = state.repositorys.filter(obj => obj.pk !== scope.row.pk)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
