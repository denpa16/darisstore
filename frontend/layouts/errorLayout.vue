<template>
    <div :class="$style.errorLayout">
        <nuxt />
    </div>
</template>

<script>
export default {
    name: 'ErrorLayout',

    components: {},
};
</script>

<style lang="scss" module>
    .errorLayout {
        height: 100dvh;
    }
</style>
