import request from '@/utils/request'

export function getOspfPeersTable(query) {
  return request({
    url: '/detail/config/route/ospf/peersTable',
    method: 'get',
    params: query
  })
}
