import request from '@/utils/request'

export function getTemplatesList(params) {
  return request({
    url: '/configManage/templates',
    method: 'get',
    params
  })
}
export function addTemplate(data) {
  return request({
    url: '/configManage/templates/',
    method: 'post',
    data
  })
}
export function updateTemplate(data) {
  return request({
    url: '/configManage/templates/'+data.id,
    method: 'put',
    data
  })
}
export function saveTemplate(data) {
  return request({
    url: '/configManage/templatesData/'+data.id,
    method: 'put',
    data
  })
}
export function deleteTemplate(id) {
  return request({
    url: '/configManage/templates/'+id,
    method: 'delete',
  })
}
