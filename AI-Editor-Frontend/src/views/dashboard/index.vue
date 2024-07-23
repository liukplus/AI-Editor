<template>
  <div class="app-container">
    <!-- <h1>Vue3-Element-Admin-Thin</h1> -->
    <router-view/>
    <Extended/>
  </div>
</template>

<script setup lang="ts">
import Extended from '@/views/editor/ExtendedEditor.vue'
defineOptions({
  name: "Dashboard",
  components: Extended,
  inheritAttrs: false,
});
</script>

<style lang="scss" scoped></style>
