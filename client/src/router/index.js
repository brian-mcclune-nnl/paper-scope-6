import { computed } from "vue"
import { createWebHistory, createRouter } from "vue-router"
import { PublicClientApplication } from "@azure/msal-browser";
import store from "../store"
import Home from "../views/Home.vue"
import Unauthenticated from "../views/Unauthenticated.vue"

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/unauthenticated',
    component: Unauthenticated
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const msalConfig = computed(() => store.state.msal.config);
const account = computed(() => store.state.msal.account);

// The msalInstance gets mutated when loginPopup() is called
// which means if made an attribute of the Vuex store state,
// it causes errors even when called in a mutation.
// The workaround is to have a global instance somewhere else
// in the application.
const msalInstance = new PublicClientApplication(msalConfig.value);

router.beforeEach(async (to, from) => {
  if (to.path !== '/unauthenticated' && account.value === null) {
    try {
      await store.dispatch('msal/login', msalInstance)
    } catch (error) {
      console.log(error)
      return '/unauthenticated'
    }
  }
})

export default router
