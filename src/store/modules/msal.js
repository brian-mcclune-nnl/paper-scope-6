import {
  PublicClientApplication,
  BrowserAuthError,
  InteractionRequiredAuthError
} from "@azure/msal-browser";

// The msalInstance gets mutated when loginPopup() is called
// which means if made an attribute of the Vuex store state,
// it causes errors even when called in a mutation.
// The workaround is to have a global instance somewhere else
// in the application.
var msalInstance = null;

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
  account: null,
  instanceCreated: false
})

// getters
const getters = {
  username(state) {
    if (state.account === null) return null;
    const claims = state.account.idTokenClaims;
    return `${claims.given_name} ${claims.family_name}`;
  }
}

// mutations
const mutations = {
  createInstance(state) {
    if (!state.instanceCreated) {
      msalInstance = new PublicClientApplication(state.config);
      state.instanceCreated = true;
    }
  },
  login(state, account) {
    state.account = account;
    msalInstance.setActiveAccount(account);
  }
}

// actions
const actions = {
  createInstance(context) {
    context.commit('createInstance');
  },
  async login({ commit, state }) {
    if (!state.instanceCreated) commit('createInstance');
    const loginRequest = {
      scopes: state.scopes,
      loginHint: state.account ? state.account.username : ""
    };
    let loginResponse = null;
    try {
      loginResponse = await msalInstance.ssoSilent(loginRequest)
    } catch (error) {
      if (!error instanceof InteractionRequiredAuthError &&
          !error instanceof BrowserAuthError )
        throw error;
      loginResponse = await msalInstance.loginPopup(loginRequest);
    }
    commit('login', loginResponse.account);
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
