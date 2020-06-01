import request from '@/plugin/axios'

export function GetRecommend (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/getrecommend/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
