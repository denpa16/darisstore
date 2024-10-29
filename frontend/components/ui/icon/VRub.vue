<script setup lang="ts">
/**
 * Позволяет отображать различные виды символов рубля.<br>
 * Символы берутся из шрифта PT-Rouble, в котором все кириллические буквы заменены на знак: ₽
 * @version 1.0.0
 * @displayName VRub
 */

// #region Imports
import type { VRubProps } from './types.ts';
import { useDeviceStore } from '@idaproject/core/store/device'; // #endregion
// #endregion

// #region Props
const { symbol = 'base' } = defineProps<VRubProps>();
// #endregion

const { isCrawler } = useDeviceStore();

// #region Data
const views = {
    base: 'Р ',
    additional: 'А',
};
// #endregion

// #region Computed
const displayedSymbol = computed(() => {
    // Если это поисковый бот, то отдаем ему знак рубля
    if (isCrawler) {
        return '₽';
    }

    // Если это предустановленный символ
    if (views[symbol as keyof typeof views]) {
        return views[symbol as keyof typeof views];
    } else { // Если кастомный
        return symbol || 'Р';
    }
});
// #endregion
</script>

<template>
    <span :class="$style.VRub">
        {{ displayedSymbol }}
    </span>
</template>

<style lang="scss" module>
    .VRub {
        font-family: PT-Rouble-Sans, sans-serif;
    }
</style>
