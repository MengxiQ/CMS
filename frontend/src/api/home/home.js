import request from '@/utils/request'

export function getList(query) {
  return request({
    url: 'admin/statistica',
    method: 'get',
    params: query
  })
}
