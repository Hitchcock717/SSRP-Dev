import request from '@/plugin/axios'

export function DeleteCollection (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/deletecollection/',
    method: 'delete',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
