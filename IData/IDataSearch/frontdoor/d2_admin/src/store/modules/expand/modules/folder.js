import folderService from '@api/demo/folder/folderService'

const state = {
  folders: []
}

const getters = {
  folders: state => {
    return state.folders
  }
}

const actions = {
  getFolders ({ commit }) {
    folderService.fetchFolder()
      .then(folders => {
        commit('setFolders', folders)
      })
  },
  deleteFolder ({ commit }, repoId) {
    folderService.deleteFolder(repoId)
    commit('deleteFolder', repoId)
  }
}

const mutations = {
  setFolders (state, folders) {
    state.folders = folders
  },
  deleteFolder (state, scope) {
    state.folders.splice(scope.$index, 1)
    state.folders = state.folders.filter(obj => obj.pk !== scope.row.pk)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
