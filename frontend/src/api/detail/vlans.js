import request from '@/utils/request'

export function getVlans(qurey) {
  return request({
    url: '/detail/config/vlans',
    method: 'get',
    params: qurey
  })
}

export function createVlans(data) {
  return request({
    url: '/detail/config/vlans',
    method: 'post',
    data
  })
}

export function deleteVlans(data) {
  return request({
    url: '/detail/config/vlans/' + data.vlanId,
    method: 'delete',
    data
  })
}

