import api from '@/api/demo/index'

export default {
  fetchFolder () {
    return api.get(`folder/`)
      .then(response => response.data)
  },
  deleteFolder (scope) {
    return api.delete(`folder/${scope.row.pk}`)
      .then(response => response.data)
  }
}
