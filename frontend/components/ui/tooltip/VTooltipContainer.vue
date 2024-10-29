<script setup lang="ts">

import type { VTooltipContainerProps } from '~/components/ui/tooltip/types';

const {
    hasArrow,
    arrowPosition,
} = defineProps<VTooltipContainerProps>();

const $style = useCssModule();
const classList = computed(() => [
    {
        [$style[`_${arrowPosition}`]]: arrowPosition,
    },
]);
</script>

<template>
    <div :class="[$style.VTooltipContainer, classList]">
        <slot />
        <div
            v-if="hasArrow"
            :class="$style.arrow"
        >
            <VIcon name="mock-arrow-top" size="custom" />
        </div>
    </div>
</template>

<style module lang="scss">
    .VTooltipContainer {
        position: relative;
        border-radius: 1.2rem;
        background-color: $base-0;
        box-shadow: 4px 4px 33px -3px rgb(34 60 80 / 20%);

        &._bottom {
            .arrow {
                top: auto;
                bottom: -1.2rem;
                transform: rotate(180deg) translateX(-50%);
            }
        }

        &._topRight {
            .arrow {
                right: 4.4rem;
            }
        }
    }

    .arrow {
        position: absolute;
        top: -1.2rem;
        right: 50%;
        z-index: 1;
        transform: translateX(-50%);

        & > svg {
            width: 1.2rem;
            height: 1rem;
            color: $base-0;
        }
    }
</style>
