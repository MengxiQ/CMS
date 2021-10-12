import request from '@/utils/request'

// 获取ospf高级配置信息
export function getOspfAdvance(query) {
  return request({
    url: '/detail/config/route/ospf/advance',
    method: 'get',
    params: query
  })
}
// 获取ospf缺省路由发布信息
export function getOspfDefaultAdvise(query) {
  return request({
    url: '/detail/config/route/ospf/defaultAdvise',
    method: 'get',
    params: query
  })
}

export function createOspfDefaultAdvise(data) {
  return request({
    url: '/detail/config/route/ospf/defaultAdvise',
    method: 'post',
    data
  })
}
