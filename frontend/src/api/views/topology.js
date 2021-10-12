import request from '@/utils/request'

export function getTopologyList(query) {
  return request({
    url: '/views/topology',
    method: 'get',
    params: query
  })
}
export function createTopology(data) {
  return request({
    url: '/views/topology/',
    method: 'post',
    data
  })
}
export function deleteTopology(data) {
  return request({
    url: '/views/topology/' + data.id,
    method: 'delete',
    data
  })
}
export function updateTopology(data) {
  return request({
    url: '/views/topology/' + data.id,
    method: 'put',
    data
  })
}

export function pingHost(query) {
  return request({
    url: '/views/topology/ping/',
    method: 'get',
    params: query
  })
}
