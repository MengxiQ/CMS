import request from '@/utils/request'

// export function gather(ip) {
//   return request({
//     url: 'detail/config/gather',
//     method: 'get',
//     params: {
//       ip
//     }
//   })
// }

// export function getinterfacesConfigByIP(ip) {
//   return request({
//     url: 'detail/config/interfaces',
//     method: 'get',
//     params: {
//       ip
//     }
//   })
// }
// 接口监控信息
export function getInterfaceMonitoring(query) {
  return request({
    url: 'detail/config/interfaces/monitoring',
    method: 'get',
    params: query
  })
}

/**
 * 通用接口
 * **/
export function getCommonInterfaces(query) {
  return request({
    url: 'detail/config/interfaces/common',
    method: 'get',
    params: query
  })
}
export function updateCommonInterface(data) {
  return request({
    url: 'detail/config/interfaces/common',
    method: 'put',
    data
  })
}
export function createCommonInterface(data) {
  return request({
    url: 'detail/config/interfaces/common',
    method: 'post',
    data
  })
}
export function deleteCommonInterface(data) {
  return request({
    url: 'detail/config/interfaces/common',
    method: 'delete',
    data
  })
}
/**
 * 以太接口
 * **/
export function getEthernetInterfaces(query) {
  return request({
    url: 'detail/config/interfaces/ethernet',
    method: 'get',
    params: query
  })
}
export function createEthernetInterface(data) {
  return request({
    url: 'detail/config/interfaces/ethernet',
    method: 'post',
    data
  })
}
export function deleteEthernetInterface(data) {
  return request({
    url: 'detail/config/interfaces/ethernet',
    method: 'delete',
    data
  })
}
/**
 * Eth-trunk接口
 * **/
export function getEthTrunkInterfaces(query) {
  return request({
    url: 'detail/config/interfaces/eth_trunk',
    method: 'get',
    params: query
  })
}
export function createEthTrunkInterface(data) {
  return request({
    url: 'detail/config/interfaces/eth_trunk',
    method: 'post',
    data
  })
}
export function deleteEthTrunkInterface(data) {
  return request({
    url: 'detail/config/interfaces/eth_trunk',
    method: 'delete',
    data
  })
}
/**
 * TrunkMemberIf接口成员
 * **/
export function getEthTrunkMember(query) {
  return request({
    url: 'detail/config/interfaces/eth_trunk/trunk_member',
    method: 'get',
    params: query
  })
}
export function createTrunkMember(data) {
  return request({
    url: 'detail/config/interfaces/eth_trunk/trunk_member',
    method: 'post',
    data
  })
}
export function deleteTrunkMember(data) {
  return request({
    url: 'detail/config/interfaces/eth_trunk/trunk_member',
    method: 'delete',
    data
  })
}
