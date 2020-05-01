import request from '@/plugin/axios'

export function GetFolder (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/getfolder/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
