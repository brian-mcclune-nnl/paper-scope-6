<template>
  <div
    v-if="username"
    class="navbar-item has-dropdown is-hoverable"
  >
    <a class="navbar-link">{{ username }}</a>
    <div class="navbar-dropdown">
      <a class="navbar-item" href="#">
        Profile
      </a>
      <a class="navbar-item" href="#">
        Sign out
      </a>
    </div>
  </div>
  <div
    v-else
    class="navbar-item"
  >
    <div class="buttons">
      <button class="button">
        <span class="icon">
          <i class="fas fa-sign-in-alt"></i>
        </span>
        <span>Sign in</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const username = computed(() => store.getters['msal/username'])
</script>
