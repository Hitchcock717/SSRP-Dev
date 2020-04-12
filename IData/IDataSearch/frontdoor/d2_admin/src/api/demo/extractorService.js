import api from '@/api/demo/index'

export default {
  fetchExtractors () {
    return api.get(`extract/`)
      .then(response => response.data)
  },
  deleteExtractor (extrId) {
    return api.delete(`extractors/${extrId}`)
      .then(response => response.data)
  }
}
