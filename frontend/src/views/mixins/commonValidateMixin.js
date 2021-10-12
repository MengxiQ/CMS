import { isArray, isString } from '@/utils/validate'
import { parseTime } from '@/utils'
/**
 * 数据类型验证和转换相关
 * **/
export const commonValidateMixin = {
  methods: {
    isArray(o) {
      return isArray(o)
    },
    parseTime(time, format) {
      // 如果time为字符串，需要先转换成Date对象
      let time_obj = time
      if (isString(time)) {
        time_obj = new Date(Date.parse(time))
      }
      return parseTime(time_obj, format)
    }
  }
}
