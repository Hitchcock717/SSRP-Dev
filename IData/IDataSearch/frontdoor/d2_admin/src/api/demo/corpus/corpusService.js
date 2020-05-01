import api from '@/api/demo/index'

export default {
  postCorpus (payload) {
    return api.post(`getcorpus/`, payload)
      .then(response => response.data)
  },
  deleteCorpus (scope) {
    return api.delete(`corpus/${scope.row.pk}`)
      .then(response => response.data)
  }
}
