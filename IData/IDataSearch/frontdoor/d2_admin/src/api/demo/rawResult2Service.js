import request from '@/plugin/axios'

export function GetRawResult (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/rawresult/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
