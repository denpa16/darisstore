import { defineNuxtPlugin } from '#app';
import Resize from '~/directives/resize';
import Intersect from '~/directives/intersect';

export default defineNuxtPlugin(nuxtApp => {
    nuxtApp.vueApp.directive('resize', Resize);
    nuxtApp.vueApp.directive('Intersect', Intersect);
});
