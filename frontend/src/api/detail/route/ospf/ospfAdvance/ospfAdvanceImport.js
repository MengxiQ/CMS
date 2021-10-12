import request from '@/utils/request'

export function getOspfAdvanceImport(query) {
  return request({
    url: '/detail/config/route/ospf/advance/import',
    method: 'get',
    params: query
  })
}

export function createOspfAdvanceImport(data) {
  return request({
    url: '/detail/config/route/ospf/advance/import',
    method: 'post',
    data
  })
}

export function deleteOspfAdvanceImport(data) {
  return request({
    url: '/detail/config/route/ospf/advance/import',
    method: 'delete',
    data
  })
}
