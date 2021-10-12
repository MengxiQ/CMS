import request from '@/utils/request'

export function fetchNetconfuserList(query) {
  return request({
    url: 'asset/equipment/netconfuser/',
    method: 'get',
    params: query
  })
}

export function getNetconfuserbyIp(ip) {
  return request({
    url: 'asset/equipment/netconfuser/',
    method: 'get',
    params: {
      ip
    }
  })
}

