import api from '@/api/demo/index'

export default {
  fetchCollection () {
    return api.get(`collection/`)
      .then(response => response.data)
  },
  deleteCollection (scope) {
    return api.delete(`collection/${scope.row.pk}`)
      .then(response => response.data)
  }
}
