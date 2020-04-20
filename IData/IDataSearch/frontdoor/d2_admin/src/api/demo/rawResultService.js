import api from '@/api/demo/index'

export default {
  fetchrawResult () {
    return api.get(`rawresult/`)
      .then(response => response.data)
  }
}
