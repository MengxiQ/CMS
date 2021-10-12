import request from '@/utils/request'

export function getAlarmList(query) {
  return request({
    url: '/detail/config/monitoring/alarm',
    method: 'get',
    params: query
  })
}

export function getBoardResStates(ip) {
  return request({
    url: '/detail/config/monitoring/boardResStates',
    method: 'get',
    params: {
      ip
    }
  })
}

export function getSystemInfo(ip) {
  return request({
    url: '/detail/config/monitoring/systemInfo',
    method: 'get',
    params: {
      ip
    }
  })
}

export function updateSystemInfo(data) {
  return request({
    url: '/detail/config/monitoring/systemInfo',
    method: 'post',
    data
  })
}

export function getSysLog(query) {
  return request({
    url: '/detail/config/monitoring/syslog',
    method: 'get',
    params: query
  })
}
