import { createStore, createLogger } from 'vuex'
import msal from './modules/msal'

const debug = process.env.NODE_ENV !== 'production'

export default createStore({
  modules: { msal },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})
