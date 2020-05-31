import request from '@/plugin/axios'

export function AddProject (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/addproject/',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
