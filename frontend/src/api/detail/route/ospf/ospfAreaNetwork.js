import request from '@/utils/request'

export function getOspfAreaNetwork(query) {
  return request({
    url: '/detail/config/route/ospf/area/network',
    method: 'get',
    params: query
  })
}

export function createOspfAreaNetwork(data) {
  return request({
    url: '/detail/config/route/ospf/area/network',
    method: 'post',
    data
  })
}

export function deleteOspfAreaNetwork(data) {
  return request({
    url: '/detail/config/route/ospf/area/network',
    method: 'delete',
    data
  })
}
