import request from '@/plugin/axios'

export function SetPwd (data) {
  return request({
    url: '/pwd',
    method: 'post',
    data
  })
}
