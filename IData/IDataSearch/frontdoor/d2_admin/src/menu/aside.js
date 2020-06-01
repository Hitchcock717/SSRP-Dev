// 菜单 侧边栏
export default [
  { path: '/index', title: '欢迎页', icon: 'home' },
  {
    title: '步骤一: 初始化',
    icon: 'folder-o',
    children: [
      { path: '/transition1', title: '搜索方式', icon: 'tags' },
      { path: '/complete', title: '完成创建', icon: 'tag' }
    ]
  },
  {
    title: '步骤二: 检索',
    icon: 'folder-o',
    children: [
      { path: '/simplesearch', title: '简单检索结果', icon: 'tag' },
      { path: '/subrepo', title: '创建子库', icon: 'tag' },
      { path: '/detailsearch', title: '高级检索结果', icon: 'tag' }
    ]
  },
  {
    title: '步骤三: 分析',
    icon: 'folder-o',
    children: [
      { path: '/analysis', title: '分析方式', icon: 'tag' }
    ]
  },
  {
    title: '步骤四: 推荐',
    icon: 'folder-o',
    children: [
      { path: '/personal', title: '个人中心', icon: 'tag' },
      { path: '/daily', title: '每日推荐', icon: 'tag' },
      { path: '/folder', title: '收藏夹', icon: 'tag' },
      { path: '/repository', title: '词表库', icon: 'tag' },
      { path: '/filerepo', title: '论文库', icon: 'tag' },
      { path: '/project', title: '项目库', icon: 'tag' }
    ]
  }
]
