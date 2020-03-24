const userDB = [
  { username: 'admin', password: 'admin', email: 'abc', authcode: 'Zxt1', uuid: 'admin-uuid', name: 'Admin' },
  { username: 'editor', password: 'editor', email: 'abc', authcode: 'Zxt1', uuid: 'editor-uuid', name: 'Editor' },
  { username: 'user1', password: 'user1', email: 'abc', authcode: 'Zxt1', uuid: 'user1-uuid', name: 'User1' }
]

export default [
  {
    path: '/api/auth',
    method: 'post',
    handle ({ body }) {
      const user = userDB.find(e => e.authcode === body.authcode)
      if (user) {
        return {
          code: 0,
          msg: '认证成功',
          data: {
            ...user,
            token: '8dfhassad0asdjwoeiruty'
          }
        }
      } else {
        return {
          code: 401,
          msg: '认证密码错误',
          data: {}
        }
      }
    }
  }
]
