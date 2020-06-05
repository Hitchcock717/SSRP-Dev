import request from '@/utils/noloading'

export function Scrapy (data) {
  return request({
    url: 'http://127.0.0.1:8000/api/scrapy/',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data
  })
}
