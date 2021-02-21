import vue from '@vitejs/plugin-vue'
import fs from 'fs'

/**
 * @type {import('vite').UserConfig}
 */
export default {
  plugins: [vue()],
  server: {
    https: {
      pfx: fs.readFileSync('./paperscope.pfx'),
      passphrase: 'dochunting'
    }
  }
}
