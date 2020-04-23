import api from '@/api/demo/index'

export default {
  fetchfilterResult () {
    return api.get(`filteresult/`)
      .then(response => response.data)
  }
}
