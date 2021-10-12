import request from '@/utils/request'

export function getOspfArea(query) {
  return request({
    url: '/detail/config/route/ospf/area',
    method: 'get',
    params: query
  })
}

export function createOspfArea(data) {
  return request({
    url: '/detail/config/route/ospf/area',
    method: 'post',
    data
  })
}

export function deleteOspfArea(data) {
  return request({
    url: '/detail/config/route/ospf/area',
    method: 'delete',
    data
  })
}
