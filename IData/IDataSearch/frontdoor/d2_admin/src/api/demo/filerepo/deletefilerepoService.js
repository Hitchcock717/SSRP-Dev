import request from '@/plugin/axios'

export function DeleteFilerepo (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/deletefilerepo/',
    method: 'delete',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
