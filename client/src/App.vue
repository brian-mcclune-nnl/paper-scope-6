<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <button @click="signIn">Signed in as: {{ username }}</button>
  <button @click="getMsg">Refresh Message</button>
  <HelloWorld :msg="msg" />
</template>

<script setup>
import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios'
import { onMounted, ref, computed } from 'vue';
import { useStore } from 'vuex';
import { PublicClientApplication } from '@azure/msal-browser';

const store = useStore();
const msg = ref("Hello Vue 3 + Vite");
const msalApp = new PublicClientApplication(store.state.msal.config);

const username = computed(() => {
  if (store.state.msal.account === null) return '<unknown';
  else {
    const claims = store.state.msal.account.idTokenClaims;
    return `${claims.given_name} ${claims.family_name}`;
  }
};

const getMsg = () => {
  // TODO: pull API endpoint definitions out of here
  const endpoint = import.meta.env.PROD
    ? 'https://dochunt-fast-api.azurewebsites.net/'
    : 'http://127.0.0.1:21383/';

  let headers = { from: 'bpmcclune@gmail.com' };

  if (store.state.msal.account !== null) {
    const scopes = ['https://clunacy.onmicrosoft.com/' +
      '7ea70574-6eb1-42f2-ab65-d88d33884ccb/user.impersonate'];
    msalApp.acquireTokenSilent({ account: store.state.msal.account, scopes })
      .then((res) => {
        console.log(res);
        headers['Authorization'] = `Bearer ${res.idToken}`;
        return axios.get(endpoint, { headers });
      })
      .then((res) => {
        console.log(res);
        msg.value = res.data.message;
      })
      .catch((err) => {
        console.log(err);
      });
  }
}

const signIn = () => {
  msalApp.loginPopup({})
    .then((res) => {
      console.log(res);
      if (res !== null) {
        store.dispatch('msal/setAccount', res.account);
        msalApp.setActiveAccount(res.account);
      } else {
        const allAccounts = msalApp.getAllAccounts();
        store.dispatch('msal/setAccount', allAccounts[0]);
        msalApp.setActiveAccount(allAccounts[0]);
      }
    })
    .catch((err) => {
      console.log(err);
    });
}

onMounted(getMsg);
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>