
import request from '@/utils/request'

export function getPingResult(query) {
  return request({
    url: '/detail/config/test/ping',
    method: 'get',
    params: query
  })
}
export function creataPingTest(data) {
  return request({
    url: '/detail/config/test/ping',
    method: 'post',
    data
  })
}
export function deletePingTest(data) {
  return request({
    url: '/detail/config/test/ping',
    method: 'delete',
    data
  })
}
