const userDB = [
  { username: 'admin', password: 'admin', email: 'abc', authcode: 'Zxt1', newpassword: 'zxt', uuid: 'admin-uuid', name: 'Admin' },
  { username: 'editor', password: 'editor', email: 'abc', authcode: 'Zxt1', uuid: 'editor-uuid', name: 'Editor' },
  { username: 'user1', password: 'user1', email: 'abc', authcode: 'Zxt1', uuid: 'user1-uuid', name: 'User1' }
]

export default [
  {
    path: '/api/pwd',
    method: 'post',
    handle ({ body }) {
      const user = userDB.find(e => e.newpassword !== body.newpassword)
      if (user) {
        return {
          code: 0,
          msg: '设置成功',
          data: {
            ...user,
            token: '8dfhassad0asdjwoeiruty'
          }
        }
      } else {
        return {
          code: 401,
          msg: '密码重复',
          data: {}
        }
      }
    }
  }
]
