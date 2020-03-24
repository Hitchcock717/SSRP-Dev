import { AuthCode } from '@api/sys.auth'

export default {
  namespaced: true,
  actions: {
    /**
     * @description 认证密码验证
     */
    auth ({ dispatch }, {
      authcode = ''
    } = {}) {
      return new Promise((resolve, reject) => {
        // 开始请求认证密码接口
        AuthCode({
          authcode
        })
          .then(async res => {
            // 结束
            resolve()
          })
          .catch(err => {
            console.log('err: ', err)
            reject(err)
          })
      })
    }
  }
}
