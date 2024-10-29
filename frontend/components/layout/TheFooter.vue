<script setup lang="ts">
import LogoIda from '@/components/common/LogoIda.vue';
</script>

<template>
    <div :class="$style.TheFooter">
        <div :class="[$style.wrapper, 'container']">
            <LogoIda to="/" />
        </div>
    </div>
</template>

<style lang="scss" module>
    .TheFooter {
        position: relative;
        z-index: 3;
        height: 20rem;
        background-color: $base-100;
    }

    .wrapper {
        display: flex;
        align-items: flex-end;
        justify-content: right;
        height: 100%;
        padding: 3.2rem;
    }
</style>
