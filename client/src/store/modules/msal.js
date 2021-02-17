import {
  BrowserAuthError,
  InteractionRequiredAuthError
} from "@azure/msal-browser";

// initial state
const state = () => ({
  config: {
    auth: {
      clientId: 'f95c6431-ef71-4809-ab02-0c94c11a71ee',
      authority:
      'https://clunacy.b2clogin.com/clunacy.onmicrosoft.com/' +
      'B2C_1_dochunt_signupsignin',
      knownAuthories: 'clunacy.b2clogin.com',
      redirectUri: import.meta.env.PROD
        ? 'https://dochunt-vue3-spa.azurewebsites.net/'
        : 'https://localhost:3000/'
    },
    cache: {
      cacheLocation: 'localStorage',
    },
  },
  scopes: [
    'https://clunacy.onmicrosoft.com/' +
    '7ea70574-6eb1-42f2-ab65-d88d33884ccb/user.impersonate',
  ],
  account: null
})

// getters
const getters = {}

// mutations
const mutations = {
  login(state, { account, instance }) {
    state.account = account;
    instance.setActiveAccount(account);
  }
}

// actions
const actions = {
  createInstance(context){
    context.commit('createInstance');
  },
  async login({ commit, state }, instance){
    const loginRequest = {
      scopes: state.scopes,
      loginHint: state.account ? state.account.username : ""
    };
    let loginResponse = null;
    try {
      loginResponse = await instance.ssoSilent(loginRequest)
    } catch (error) {
      if (!error instanceof InteractionRequiredAuthError &&
          !error instanceof BrowserAuthError )
        throw error;
      loginResponse = await instance.loginPopup(loginRequest);
    }
    commit('login', { account: loginResponse.account, instance });
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
