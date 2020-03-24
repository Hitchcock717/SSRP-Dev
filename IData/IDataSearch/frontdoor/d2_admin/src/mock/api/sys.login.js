// 自定义管理员数据库
const userDB = [
  { username: 'admin', password: 'admin', email: '123@qq.com', uuid: 'admin-uuid', name: 'Admin' },
  { username: 'editor', password: 'editor', email: 'abc@qq.com', uuid: 'editor-uuid', name: 'Editor' },
  { username: 'user1', password: 'user1', email: 'abc@qq.com', uuid: 'user1-uuid', name: 'User1' }
]

export default [
  {
    path: '/api/login',
    method: 'post',
    handle ({ body }) {
      const user = userDB.find(e => e.username === body.username && e.password === body.password && e.email === body.email)
      if (user) {
        return {
          code: 0,
          msg: '登录成功',
          data: {
            ...user,
            token: '8dfhassad0asdjwoeiruty'
          }
        }
      } else {
        return {
          code: 401,
          msg: '用户或密码错误',
          data: {}
        }
      }
    }
  }
]
