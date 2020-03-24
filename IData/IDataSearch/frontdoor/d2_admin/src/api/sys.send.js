import request from '@/plugin/axios'

export function EmailSend (data) {
  return request({
    url: '/send',
    method: 'post',
    data
  })
}
