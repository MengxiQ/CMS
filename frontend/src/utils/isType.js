
/* 判断对象是否是数组*/
export function isArray(o) {
  // console.log(o,Object.prototype.toString.call(o))
  return Object.prototype.toString.call(o) === '[object Array]'
}

