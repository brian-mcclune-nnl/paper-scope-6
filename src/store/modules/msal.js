// initial state
const state = () => ({
  config: {
    auth: {
      clientId: 'f95c6431-ef71-4809-ab02-0c94c11a71ee',
      authority:
      'https://clunacy.b2clogin.com/clunacy.onmicrosoft.com/' +
      'B2C_1_dochuntsignupsignin',
      knownAuthories: 'clunacy.b2clogin.com',
      redirectUri: import.meta.env.PROD
        ? 'https://dochunt-vue3-spa.azurewebsites.net/'
        : 'https://localhost:3000/'
    },
    cache: {
      cacheLocation: 'localStorage',
    },
  },
  accessToken: '',
  account: null
})

// getters
const getters = {}

// mutations
const mutations = {
  setAccessToken(state, token){
    state.accessToken = token;
  },
  setAccount(state, account){
    state.account = account;
  }
}

// actions
const actions = {
  setAccessToken(context, token){
    context.commit('setAccessToken', token);
  },
  setAccount(context, account){
    context.commit('setAccount', account);
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
