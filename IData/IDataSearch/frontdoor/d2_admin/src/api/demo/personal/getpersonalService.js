import request from '@/plugin/axios'

export function GetPersonal (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/getpersonal/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
