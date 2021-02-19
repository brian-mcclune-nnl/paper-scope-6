<template>
  <router-view />
</template>

<script setup>
import { useStore } from "vuex";
const store = useStore();
store.dispatch("msal/createInstance");
</script>

<style lang="scss">
@import 'bulma/css/bulma.css';
@import '@fortawesome/fontawesome-free/css/all.css';

#app {
  text-align: center;
}
</style>