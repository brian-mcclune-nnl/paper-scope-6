<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <button @click="signIn">Signed in as: {{ username }}</button>
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

const username = computed(() =>
  store.state.msal.account !== null ? store.state.msal.account.name : ''
);

const getMsg = () => {
  axios.get('http://127.0.0.1:21383')
    .then(function (res) {
      msg.value = res.data.message;
    })
    .catch(function (err) {
      console.log(err);
    });
}

const signIn = () => {
  msalApp.loginPopup({})
    .then((res) => {
      console.log('response', res);
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
      console.log('error', err);
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