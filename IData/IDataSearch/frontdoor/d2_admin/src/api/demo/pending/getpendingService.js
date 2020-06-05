import request from '@/plugin/axios'

export function GetPending (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/getpending/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
