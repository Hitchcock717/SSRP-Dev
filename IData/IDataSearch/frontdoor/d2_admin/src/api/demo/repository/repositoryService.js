import api from '@/api/demo/index'

export default {
  fetchRepository () {
    return api.get(`repository/`)
      .then(response => response.data)
  },
  deleteRepository (scope) {
    return api.delete(`repository/${scope.row.pk}`)
      .then(response => response.data)
  }
}
