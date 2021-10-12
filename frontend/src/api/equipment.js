import request from '@/utils/request'

export function fetchEquipmentList(query) {
  return request({
    url: 'asset/equipment',
    method: 'get',
    params: query
  })
}
export function updateEquipment(data) {
  return request({
    url: 'asset/equipment/' + data.id,
    method: 'put',
    data
  })
}
export function deleteEquipment(data) {
  return request({
    url: 'asset/equipment/' + data.id,
    method: 'delete'
  })
}
export function createEquipment(data) {
  return request({
    url: 'asset/equipment/',
    method: 'post',
    data
  })
}


export function createStatus(data) {
  return request({
    url: '/asset/equipment/status/',
    method: 'post',
    data
  })
}
export function updateStatus(data) {
  return request({
    url: '/asset/equipment/status/' + data.id,
    method: 'put',
    data
  })
}

export function fetchEquipmentListByIp(query) {
  return request({
    url: 'asset/equipment/equipmentByIp',
    method: 'get',
    params: query
  })
}

