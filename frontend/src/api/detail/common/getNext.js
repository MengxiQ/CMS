import request from '@/utils/request'

export function getNext(query) {
  return request({
    url: 'detail/config/get/next',
    method: 'get',
    params: query
  })
}
