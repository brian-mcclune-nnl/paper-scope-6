<template>
  <router-view />
</template>

<script setup>
import { useStore } from "vuex";
const store = useStore();
store.dispatch("msal/createInstance");
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