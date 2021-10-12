import request from '@/utils/request'

export function getBgpBase(query) {
  return request({
    url: '/detail/config/route/bgp',
    method: 'get',
    params: query
  })
}

export function createBgpBase(data) {
  return request({
    url: '/detail/config/route/bgp',
    method: 'post',
    data
  })
}

export function deleteBgpBase(data) {
  return request({
    url: '/detail/config/route/bgp',
    method: 'delete',
    data
  })
}

export function getBgpPeer(query) {
  return request({
    url: '/detail/config/route/bgp/peer',
    method: 'get',
    params: query
  })
}

export function createBgpPeer(data) {
  return request({
    url: '/detail/config/route/bgp/peer',
    method: 'post',
    data
  })
}

export function deleteBgpPeer(data) {
  return request({
    url: '/detail/config/route/bgp/peer',
    method: 'delete',
    data
  })
}

export function getNetworkPeer(query) {
  return request({
    url: '/detail/config/route/bgp/network',
    method: 'get',
    params: query
  })
}

export function createBgpNetwork(data) {
  return request({
    url: '/detail/config/route/bgp/network',
    method: 'post',
    data
  })
}

export function deleteBgpNetwork(data) {
  return request({
    url: '/detail/config/route/bgp/network',
    method: 'delete',
    data
  })
}

export function getBgpImportProtocol(query) {
  return request({
    url: '/detail/config/route/bgp/import/protocol',
    method: 'get',
    params: query
  })
}

export function createBgpImportProtocol(data) {
  return request({
    url: '/detail/config/route/bgp/import/protocol',
    method: 'post',
    data
  })
}

export function deleteBgpImportProtocol(data) {
  return request({
    url: '/detail/config/route/bgp/import/protocol',
    method: 'delete',
    data
  })
}

export function getBgpImportInstance(query) {
  return request({
    url: '/detail/config/route/bgp/import/instance',
    method: 'get',
    params: query
  })
}

export function createBgpImportInstance(data) {
  return request({
    url: '/detail/config/route/bgp/import/instance',
    method: 'post',
    data
  })
}

export function deleteBgpImportInstance(data) {
  return request({
    url: '/detail/config/route/bgp/import/instance',
    method: 'delete',
    data
  })
}

