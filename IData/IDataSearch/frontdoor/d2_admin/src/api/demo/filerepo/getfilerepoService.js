import request from '@/plugin/axios'

export function GetFilerepo (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/getfilerepo/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
