<template>
  <img alt="Vue logo" src="../assets/logo.png" />
  <HelloWorld :msg="msg" />
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import HelloWorld from "../components/HelloWorld.vue";

const store = useStore();
const account = computed(() => store.state.msal.account);
const username = computed(() => {
  if (account.value === null) return "<unknown>";
  console.log(account.value);
  const claims = account.value.idTokenClaims;
  return `${claims.given_name} ${claims.family_name}`;
});
const msg = computed(() => `Hi ${username.value} from Vue Router!`);
</script>
