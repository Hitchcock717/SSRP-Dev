import layoutHeaderAside from '@/layout/header-aside'

// 由于懒加载页面太多的话会造成webpack热更新太慢，所以开发环境不使用懒加载，只有生产环境使用懒加载
const _import = require('@/libs/util.import.' + process.env.NODE_ENV)

/**
 * 在主框架内显示
 */
const frameIn = [
  {
    path: '/',
    redirect: { name: 'index' },
    component: layoutHeaderAside,
    children: [
      // 首页
      {
        path: 'index',
        name: 'index',
        meta: {
          auth: true
        },
        component: _import('system/index')
      },
      // 演示页面
      {
        path: 'page1',
        name: 'page1',
        meta: {
          title: '创建项目',
          auth: true
        },
        component: _import('demo/page1')
      },
      {
        path: 'transition1',
        name: 'transition1',
        meta: {
          title: '搜索方式',
          auth: true
        },
        component: _import('demo/transition1')
      },
      {
        path: 'paper',
        name: 'paper',
        meta: {
          title: '论文搜索',
          auth: true
        },
        component: _import('demo/paper')
      },
      {
        path: 'corpusearch',
        name: 'corpusearch',
        meta: {
          title: '词表搜索',
          auth: true
        },
        component: _import('demo/corpus')
      },
      {
        path: 'recommend',
        name: 'recommend',
        meta: {
          title: '推荐词汇',
          auth: true
        },
        component: _import('demo/recommend')
      },
      {
        path: 'complete',
        name: 'complete',
        meta: {
          title: '完成创建',
          auth: true
        },
        component: _import('demo/complete')
      },
      {
        path: 'startsearch',
        name: 'startsearch',
        meta: {
          title: '开始检索',
          auth: true
        },
        component: _import('demo/startsearch')
      },
      {
        path: 'notice1',
        name: 'notice1',
        meta: {
          title: '等待检索结果',
          auth: true
        },
        component: _import('demo/notice1')
      },
      {
        path: 'simplesearch',
        name: 'simplesearch',
        meta: {
          title: '简单检索结果',
          auth: true
        },
        component: _import('demo/simplesearch')
      },
      {
        path: 'detail1',
        name: 'detail1',
        meta: {
          title: '简单检索详情',
          auth: true
        },
        component: _import('demo/detail1')
      },
      {
        path: 'detail2',
        name: 'detail2',
        meta: {
          title: '高级检索详情',
          auth: true
        },
        component: _import('demo/detail2')
      },
      {
        path: 'subrepo',
        name: 'subrepo',
        meta: {
          title: '创建子库',
          auth: true
        },
        component: _import('demo/subrepo')
      },
      {
        path: 'detailsearch',
        name: 'detailsearch',
        meta: {
          title: '高级检索结果',
          auth: true
        },
        component: _import('demo/detailsearch')
      },
      {
        path: 'personal',
        name: 'personal',
        meta: {
          title: '个人中心设置',
          auth: true
        },
        component: _import('demo/personal')
      },
      {
        path: 'personal1',
        name: 'personal1',
        meta: {
          title: '个人中心',
          auth: true
        },
        component: _import('demo/personal1')
      },
      {
        path: 'folder',
        name: 'folder',
        meta: {
          title: '收藏夹',
          auth: true
        },
        component: _import('demo/folder')
      },
      {
        path: 'collection',
        name: 'collection',
        meta: {
          title: '收藏夹详情',
          auth: true
        },
        component: _import('demo/collection')
      },
      {
        path: 'repository',
        name: 'repository',
        meta: {
          title: '词表库',
          auth: true
        },
        component: _import('demo/repository')
      },
      {
        path: 'corpus',
        name: 'corpus',
        meta: {
          title: '词表详情',
          auth: true
        },
        component: _import('demo/corpus')
      },
      // 系统 前端日志
      {
        path: 'log',
        name: 'log',
        meta: {
          title: '前端日志',
          auth: true
        },
        component: _import('system/log')
      },
      // 刷新页面 必须保留
      {
        path: 'refresh',
        name: 'refresh',
        hidden: true,
        component: _import('system/function/refresh')
      },
      // 页面重定向 必须保留
      {
        path: 'redirect/:route*',
        name: 'redirect',
        hidden: true,
        component: _import('system/function/redirect')
      }
    ]
  }
]

/**
 * 在主框架之外显示
 */
const frameOut = [
  // 登录 + 注册
  {
    path: '/login',
    name: 'login',
    component: _import('system/login')
  },
  {
    path: '/register',
    name: 'register',
    component: _import('system/register')
  },
  {
    path: '/reset',
    name: 'reset',
    component: _import('system/reset')
  },
  {
    path: '/send',
    name: 'send',
    component: _import('system/send')
  },
  {
    path: '/setpwd',
    name: 'setpwd',
    component: _import('system/setpwd')
  }
]
/**
 * 错误页面
 */
const errorPage = [
  {
    path: '*',
    name: '404',
    component: _import('system/error/404')
  }
]

// 导出需要显示菜单的
export const frameInRoutes = frameIn

// 重新组织后导出
export default [
  ...frameIn,
  ...frameOut,
  ...errorPage
]
