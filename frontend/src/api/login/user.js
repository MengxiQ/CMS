import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'authorizations/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/admin/user/',
    method: 'get',
    params: { token }
  })
}
// JWT 退出不需要访问后台
export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
