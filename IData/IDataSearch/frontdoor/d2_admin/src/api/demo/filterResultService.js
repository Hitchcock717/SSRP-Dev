import request from '@/plugin/axios'

export function GetFilterResult (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/filteresult/',
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}

export function GetPreRecord (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/getrecordId/',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
