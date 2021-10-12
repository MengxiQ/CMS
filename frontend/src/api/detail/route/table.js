// config/route/route/table
import request from '@/utils/request'

export function getRouteTable(ip) {
  return request({
    url: '/detail/config/route/table',
    method: 'get',
    params: {
      ip
    }
  })
}
