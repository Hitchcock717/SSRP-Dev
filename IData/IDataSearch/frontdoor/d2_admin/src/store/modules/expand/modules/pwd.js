import { SetPwd } from '@api/sys.pwd'

export default {
  namespaced: true,
  actions: {
    /**
     * @description 新密码验证
     */
    pwd ({ dispatch }, {
      newpassword = ''
    } = {}) {
      return new Promise((resolve, reject) => {
        // 开始请求新密码接口
        SetPwd({
          newpassword
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
