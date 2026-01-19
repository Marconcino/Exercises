const routes = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', component: () => import('../pages/DashboardPage.vue') },
      { path: 'bookings', component: () => import('../pages/BookingsPage.vue') },
      { path: 'tables', component: () => import('../pages/TablesPage.vue') },
      { path: 'clients', component: () => import('../pages/ClientsPage.vue') }
    ]
  },

  // Always leave this as last one
  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/ErrorNotFound.vue')
  }
]

export default routes
