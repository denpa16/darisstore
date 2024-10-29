<script setup lang="ts">
// #region Imports
import type { VTimeLineProps } from './types.ts';
// #endregion

// #region Props
const {
    horizontal,
} = defineProps<VTimeLineProps>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// Computed
const classList = computed(() => [
    {
        [$style._horizontal]: horizontal,
    },
]);
// #endregion
</script>

<template>
    <div ref="timeline" :class="[$style.VTimeLine, ...classList]">
        <slot />
    </div>
</template>

<style lang="scss" module>
    .VTimeLine {
        display: flex;
        flex-direction: column;

        &._horizontal {
            flex-direction: row;
        }
    }
</style>
