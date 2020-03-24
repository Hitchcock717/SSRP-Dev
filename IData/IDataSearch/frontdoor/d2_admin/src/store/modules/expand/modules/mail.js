import { EmailSend } from '@api/sys.send'

export default {
  namespaced: true,
  actions: {
    /**
     * @description 邮箱验证
     */
    send ({ dispatch }, {
      email = ''
    } = {}) {
      return new Promise((resolve, reject) => {
        // 开始请求登录接口
        EmailSend({
          email
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
