import request from '@/plugin/axios'

export function DeleteRepository (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/deleterepository/',
    method: 'delete',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
