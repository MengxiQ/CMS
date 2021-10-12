import request from '@/utils/request'

export function connect(query) {
  return request({
    url: 'detail/config/connect',
    method: 'get',
    params: query
  })
}
export function disconnect(data) {
  return request({
    url: 'detail/config/connect',
    method: 'delete',
    data
  })
}
