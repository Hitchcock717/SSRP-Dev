import api from '@/api/demo/index'

export default {
  fetchRecommends () {
    return api.get(`recommend/`)
      .then(response => response.data)
  },
  deleteRecommend (recomId) {
    return api.delete(`recommends/${recomId}`)
      .then(response => response.data)
  }
}
