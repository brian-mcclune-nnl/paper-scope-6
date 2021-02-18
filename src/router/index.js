import { computed } from "vue"
import { createWebHistory, createRouter } from "vue-router"
import store from "../store"
import Home from "../views/Home.vue"
import Unauthenticated from "../views/Unauthenticated.vue"

const routes = [
  {
    path: "/",
    component: Home
  },
  {
    path: "/unauthenticated",
    component: Unauthenticated
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const account = computed(() => store.state.msal.account);

router.beforeEach(async (to, from) => {
  if (to.path !== "/unauthenticated" && account.value === null) {
    try {
      await store.dispatch("msal/login")
    } catch (error) {
      console.log(error)
      return "/unauthenticated"
    }
  }
})

export default router
