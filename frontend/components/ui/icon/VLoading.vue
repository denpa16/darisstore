<script setup lang="ts">
// #region Imports
import type { VLoadingProps } from './types';
// #endregion

// #region Props
const { size = 'medium', theme = 'light' } = defineProps<VLoadingProps>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion


// #region Computed
const classList = computed(() => [
    {
        [$style[`_${size}`]]: size,
        [$style[`_${theme}`]]: theme,
    },
]);
// #endregion
</script>

<template>
    <div :class="[$style.VLoading, ...classList]"/>
</template>

<style lang="scss" module>
    .VLoading {
        display: inline-block;
        border-radius: 50%;
        border: 2px solid;
        animation: rotation 1s linear infinite;

        &._light {
            border-color: $base-0;
            border-bottom-color: transparent;
        }

        &._dark {
            border-color: $base-900;
            border-bottom-color: transparent;
        }

        &._medium {
            width: 1.6rem;
            height: 1.6rem;
        }

        &._small {
            width: 1.4rem;
            height: 1.4rem;
        }
    }

    @keyframes rotation {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }
</style>
