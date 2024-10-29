import { defineNuxtPlugin } from '#app';
import { useMainStore } from '~/store';

export default defineNuxtPlugin(async nuxtApp => {
    await useMainStore(nuxtApp.$pinia).nuxtServerInit();
});
