export default defineNuxtPlugin(nuxtApp => {
    const sentry = {
        captureException() {
            return false;
        },
    };

    nuxtApp.provide('sentry', sentry);
});
