import request from '@/plugin/axios'

export function AddCollection (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/addcollection/',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
