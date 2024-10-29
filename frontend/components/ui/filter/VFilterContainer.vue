<script setup lang="ts">
// #region Imports
import type { VFilterContainerProps } from '~/components/ui/filter/types.ts';
// #endregion

// #region Props
const {
    label = '',
    size = 'medium',
    hasMarginLeft,
} = defineProps<VFilterContainerProps>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._hasMarginLeft]: hasMarginLeft,
        [$style[`_${size}`]]: size,
    },
]);
// #endregion
</script>

<template>
    <div :class="[$style.VFilterContainer, ...classList]">
        <div
            v-if="label"
            :class="$style.label"
        >
            <span v-html="label" />
        </div>

        <div :class="$style.body">
            <slot />
        </div>
    </div>
</template>

<style lang="scss" module>
    .VFilterContainer {

        /* Sizes */
        &._medium {
            .label {
                @include text(l4);

                margin-bottom: .8rem;
            }
        }

        &._large {
            .label {
                @include text(l2-regular);

                margin-bottom: 1.6rem;
            }
        }

        /** End Sizes */

        /* Modificators */
        &._hasMarginLeft {
            .label {
                margin-left: 2rem;
            }
        }

        /** End Modificators */
    }

    .label {
        display: flex;
        line-height: 100%;
        color: $base-600;
    }
</style>
