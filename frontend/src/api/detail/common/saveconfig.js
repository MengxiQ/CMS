import request from '@/utils/request'

export function saveConfig(data) {
  return request({
    url: 'detail/config/saveconfig',
    method: 'post',
    data
  })
}
