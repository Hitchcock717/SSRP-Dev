import request from '@/plugin/axios'

export function DeleteRecommend (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/deleterecommend/',
    method: 'delete',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
