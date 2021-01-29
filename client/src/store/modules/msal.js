// initial state
const state = () => ({
  config: {
    auth: {
      clientId: '7a0d396a-c9aa-4a65-8bff-e906fef7b0c7',
      authority:
      'https://login.microsoftonline.com/07f0848e-60d0-4c23-8482-cebd7ab04d72',
    },
    cache: {
      cacheLocation: 'localStorage',
    },
  },
  accessToken: ''
})

// getters
const getters = {}

// actions
const actions = {}

// mutations
const mutations = {
  setAccessToken(state, token){
    state.accessToken = token;
  }
}
