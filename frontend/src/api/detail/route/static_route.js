import request from '@/utils/request'

export function getSatic_route(query) {
  return request({
    url: '/detail/config/route/static_route',
    method: 'get',
    params: query
  })
}

export function createSatic_route(data) {
  return request({
    url: '/detail/config/route/static_route',
    method: 'post',
    data
  })
}

export function deleteSatic_route(data) {
  return request({
    url: '/detail/config/route/static_route',
    method: 'delete',
    data
  })
}

