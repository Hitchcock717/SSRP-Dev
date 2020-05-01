import request from '@/plugin/axios'

export function AddRepository (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/addrepository/',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
