import request from '@/plugin/axios'

export function DeletePending (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/deletepending/',
    method: 'delete',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
