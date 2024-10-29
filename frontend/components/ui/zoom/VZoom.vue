<script setup lang="ts">
// #region Imports
import type { Props } from './types.ts';
// #endregion

// #region Props
const {
    color = 'black',
    disabled = false,
} = defineProps<Props>();
// #endregion
</script>

<template>
    <div :class="[$style.VZoom]">
        <VButton
            tag="button"
            :color="color"
            border
            round
            equal
            :disabled="disabled"
            :class="$style.button"
        >
            <VIcon name="mock-add" size="medium" />
        </VButton>
        <VButton
            tag="button"
            :color="color"
            border
            round
            equal
            :disabled="disabled"
            :class="$style.button"
        >
            <VIcon name="mock-substract" size="medium" />
        </VButton>
    </div>
</template>

<style lang="scss" module>
    .VZoom {
        position: relative;
        display: flex;
        flex-direction: column;
        user-select: none;
    }

    .button {
        &:not(:last-child) {
            margin-bottom: .4rem;
        }
    }
</style>
