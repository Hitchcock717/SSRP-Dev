const userDB = [
  { username: 'admin', password: 'admin', email: 'abc', uuid: 'admin-uuid', name: 'Admin' },
  { username: 'editor', password: 'editor', email: 'abc', uuid: 'editor-uuid', name: 'Editor' },
  { username: 'user1', password: 'user1', email: 'abc', uuid: 'user1-uuid', name: 'User1' }
]

export default [
  {
    path: '/api/send',
    method: 'post',
    handle ({ body }) {
      const user = userDB.find(e => e.email === body.email)
      if (user) {
        return {
          code: 0,
          msg: '发送成功',
          data: {
            ...user,
            token: '8dfhassad0asdjwoeiruty'
          }
        }
      } else {
        return {
          code: 401,
          msg: '邮箱错误',
          data: {}
        }
      }
    }
  }
]
