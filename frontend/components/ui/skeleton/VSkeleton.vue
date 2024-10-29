<script setup lang="ts">
/**
 * Компонент обертка для отображения состояния загрузки контента<br>
 * Область применения: Динамические текстовые данные, карточки.
 *
 * @version 1.0.1
 * @displayName VSkeleton
 */

// #region Imports
import type { Props } from './types.ts';
// #endregion

// #region Props
const {
    width = '100%',
    height = '40px',
    background = '#f7f7f7',
    highlight = '#fff',
    isLoading,
    sharp,
    round,
} = defineProps<Props>();

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._sharp]: sharp,
        [$style._round]: round,
    },
]);

const styleList = computed(() => ({
    main: {
        width,
        height,
        background,
    },
    highlight: {
        background: highlight,
    },
}));
// #endregion
</script>

<template>
    <transition
        name="fade"
        mode="out-in"
    >
        <div
            v-if="isLoading"
            :class="[$style.VSkeleton, classList]"
            :style="styleList.main"
        >
            <div
                :class="$style.highlight"
                :style="styleList.highlight"
            >
            </div>
        </div>

        <template v-else>
            <!-- @slot Компонент который нужно заменить "костью" -->
            <slot></slot>
        </template>
    </transition>
</template>

<style lang="scss" module>
    .VSkeleton {
        position: relative;
        overflow: hidden;
        border-radius: 1.2rem;

        .highlight {
            content: "";
            position: absolute;
            top: -25%;
            left: 0;
            display: block;
            width: 100%;
            height: 200%;
            transform: skewX(-10deg);
            animation: translate-left 1.5s infinite;

            @keyframes translate-left {
                0% {
                    left: -110%;
                    opacity: 0;
                }

                30% {
                    opacity: 1;
                }

                70% {
                    opacity: 1;
                }

                100% {
                    left: 110%;
                    opacity: 0;
                }
            }
        }

        &._sharp {
            border-radius: 0;
        }

        &._round {
            border-radius: 100%;
        }
    }
</style>
