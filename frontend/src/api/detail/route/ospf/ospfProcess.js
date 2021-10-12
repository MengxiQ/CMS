import request from '@/utils/request'

export function getOspfProcess(query) {
  return request({
    url: '/detail/config/route/ospf/process',
    method: 'get',
    params: query
  })
}

export function createOspfProcess(data) {
  return request({
    url: '/detail/config/route/ospf/process',
    method: 'post',
    data
  })
}

export function deleteOspfProcess(data) {
  return request({
    url: '/detail/config/route/ospf/process',
    method: 'delete',
    data
  })
}
