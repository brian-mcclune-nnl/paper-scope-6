// initial state
const state = () => ({
  config: {
    auth: {
      clientId: '7a0d396a-c9aa-4a65-8bff-e906fef7b0c7',
      authority:
      'https://clunacy.b2clogin.com/clunacy.onmicrosoft.com/' +
      'B2C_1_dochuntsignupsignin',
      knownAuthories: 'clunacy.b2clogin.com',
      redirectUri: 'https://localhost:3000/'
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
