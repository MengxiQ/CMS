import request from '@/utils/request'

export function getList(data) {
  return request({
    url: '/admin/users/',
    method: 'get',
    params: { data }
  })
}
export function createUser(data) {
  return request({
    url: '/admin/users/',
    method: 'post',
    data
  })
}
export function updateUser(data) {
  return request({
    url: '/admin/users/' + data.id,
    method: 'put',
    data
  })
}
export function deleteUser(id) {
  return request({
    url: '/admin/users/' + id,
    method: 'delete',
  })
}
