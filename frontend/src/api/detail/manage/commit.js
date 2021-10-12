import request from '@/utils/request'

export function commit(ip, options) {
  return request({
    url: '/detail/config/commit',
    method: 'post',
    data: {
      ip,
      options
    }
  })
}
