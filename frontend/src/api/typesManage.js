import request from '@/utils/request'

/**
 * 模板类型
 * **/
export function getTemplateTypesList(params) {
  return request({
    url: '/typeManage/templateTypes/',
    method: 'get',
    params
  })
}

export function addTemplateTypes(data) {
  return request({
    url: '/typeManage/templateTypes/',
    method: 'post',
    data
  })
}

export function updateTemplateTypes(data) {
  return request({
    url: '/typeManage/templateTypes/' + data.id,
    method: 'put',
    data
  })
}

export function deleteTemplateTypes(id) {
  return request({
    url: '/typeManage/templateTypes/' + id,
    method: 'delete'
  })
}

/**
 * 设备型号
 * **/
export function getUnitTypesList(params) {
  return request({
    url: '/typeManage/unitTypesTypes/',
    method: 'get',
    params
  })
}

export function addUnitType(data) {
  return request({
    url: '/typeManage/unitTypesTypes/',
    method: 'post',
    data
  })
}

export function updateUnitType(data) {
  return request({
    url: '/typeManage/unitTypesTypes/' + data.id,
    method: 'put',
    data
  })
}

export function deleteUnitType(id) {
  return request({
    url: '/typeManage/unitTypesTypes/' + id,
    method: 'delete'
  })
}

/**
 * 功能列表
 * **/
export function getFunctionsList(params) {
  return request({
    url: '/typeManage/functions/',
    method: 'get',
    params
  })
}

export function addFunction(data) {
  return request({
    url: '/typeManage/functions/',
    method: 'post',
    data
  })
}

export function updateFunction(data) {
  return request({
    url: '/typeManage/functions/' + data.id,
    method: 'put',
    data
  })
}

export function deleteFunction(id) {
  return request({
    url: '/typeManage/functions/' + id,
    method: 'delete'
  })
}

/**
 * 设备类型
 * **/
export function getNeTypesList(params) {
  return request({
    url: '/typeManage/neTypes/',
    method: 'get',
    params
  })
}

export function addNeType(data) {
  return request({
    url: '/typeManage/neTypes/',
    method: 'post',
    data
  })
}

export function updateNeType(data) {
  return request({
    url: '/typeManage/neTypes/' + data.id,
    method: 'put',
    data
  })
}

export function deleteNeType(id) {
  return request({
    url: '/typeManage/neTypes/' + id,
    method: 'delete'
  })
}

/**
 * 厂商类型
 * **/
export function getVendorTypesList(params) {
  return request({
    url: '/typeManage/vendorTypes/',
    method: 'get',
    params
  })
}

export function addVendorType(data) {
  return request({
    url: '/typeManage/vendorTypes/',
    method: 'post',
    data
  })
}

export function updateVendorType(data) {
  return request({
    url: '/typeManage/neTypes/' + data.id,
    method: 'put',
    data
  })
}

export function deleteVendorType(id) {
  return request({
    url: '/typeManage/vendorTypes/' + id,
    method: 'delete'
  })
}

