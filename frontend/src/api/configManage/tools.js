import request from '@/utils/request'

export function sendXmlConfig(data) {
  return request({
    url: '/configManage/xmlTools/',
    method: 'post',
    data
  })
}
export function GenerateConfig(data) {
  return request({
    url: '/configManage/GenerateConfig/',
    method: 'post',
    data
  })
}
export function ConfigXml(data) {
  return request({
    url: '/configManage/ConfigXml/',
    method: 'post',
    data
  })
}
