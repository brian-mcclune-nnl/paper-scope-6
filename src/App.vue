<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <HelloWorld :msg="msg" />
</template>

<script setup>
import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue';

const msg = ref("Hello Vue 3 + Vite");

const getMsg = () => {
  axios.get('http://127.0.0.1:21383')
    .then(function (res) {
      msg.value = res.data.message;
    })
    .catch(function (err) {
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