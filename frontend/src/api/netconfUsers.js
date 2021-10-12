import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: 'asset/equipment/netconfuser/',
    method: 'get',
    params: query
  })
}
export function createNetconfuser(data) {
  return request({
    url: 'asset/equipment/netconfuser/',
    method: 'post',
    data
  })
}
export function updateNetconfuser(data) {
  return request({
    url: 'asset/equipment/netconfuser/' + data.id,
    method: 'put',
    data
  })
}
export function deleteNetconfuser(id) {
  return request({
    url: 'asset/equipment/netconfuser/'+ id,
    method: 'delete',
  })
}

export function batchUsers(data){
  return request({
    url: 'asset/equipment/batchUsers/',
    method: 'post',
    data
  })
}
