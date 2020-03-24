import request from '@/plugin/axios'

export function AuthCode (data) {
  return request({
    url: '/auth',
    method: 'post',
    data
  })
}
