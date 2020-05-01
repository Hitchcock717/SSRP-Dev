import request from '@/plugin/axios'

export function DeleteFolder (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/deletefolder/',
    method: 'delete',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
