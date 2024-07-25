import { createWebHistory, createRouter } from 'vue-router'

const routes = [
  { path: '/', component: ScenarioList },
  {
    path: '/scenarios/index',
    name: 'Scenario Index',
    component: ScenarioList,
    meta: { requiresScenarioSelection: false }
  },
  {
    path: '/scenarios/add',
    name: 'New Scenario',
    component: ScenarioNew,
    meta: { requiresScenarioSelection: false }
  },
  {
    path: '/scenarios/overview/:uuid?',
    name: 'Scenario Overview',
    component: ScenarioOverview,
    meta: { requiresScenarioSelection: true },
    props: true
  },
  {
    path: '/scenarios/designer/:uuid?',
    name: 'Scenario Designer',
    component: ScenarioDesigner,
    meta: { requiresScenarioSelection: true },
    props: true
  },
  { path: '/injects/tester/:uuid?', name: 'Inject Tester', component: InjectTester, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from) => {
  if (to.path === '/') {
    return { path: '/scenarios/index' }
  }
  if (!hasScenarios()) {
    fetchScenarios()
  }
  if (
    from.name == undefined &&
    ['Scenario Overview', 'Scenario Designer'].includes(to.name) &&
    to?.params?.uuid !== undefined
  ) {
    store.selected_scenario = to.params.uuid
  }
  if (to?.meta?.requiresScenarioSelection === true && store.selected_scenario === null) {
    return { path: '/scenarios/index' }
  }
  if (to.matched.length == 0) {
    return { path: '/scenarios/index' }
  }
})
