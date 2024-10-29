<script setup lang="ts">
// #region Imports
import type { VTimeLineItemProps } from './types.ts';
// #endregion

// #region Props
const {
    index = 0,
    progress = 0,
    active = false,
    complete,
    horizontal,
} = defineProps<VTimeLineItemProps>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// Computed
const classList = computed(() => [
    {
        [$style._active]: progress > 0 || active,
        [$style._horizontal]: horizontal,
    },
]);

const lineFillStyle = computed(() => ({
    width: horizontal ? `${progress}%` : '100%',
    height: horizontal ? '100%' : `${progress}%`,
}));
// #endregion
</script>

<template>
    <div :class="[$style.VTimeLineItem, ...classList]">
        <div :class="$style.progress">
            <div :class="$style.line">
                <div
                    :class="$style.lineFill"
                    :style="lineFillStyle"
                >
                </div>
            </div>
            <div
                :class="[$style.circle]"
            >
                <template v-if="complete">
                    <VIcon name="mock-checkbox" />
                </template>
                <template v-else>
                    {{ index }}
                </template>
            </div>
        </div>
        <div :class="$style.content">
            <slot />
        </div>
    </div>
</template>

<style lang="scss" module>
    $active: $primary-100;
    $secondary: $base-100;

    .VTimeLineItem {
        display: flex;
        min-height: 6.9rem;

        &:last-child .line {
            opacity: 0;
        }

        &:not(:last-child) .content {
            padding-bottom: 60px;

            @include respond-to(tablet) {
                padding-bottom: 52px;
            }

            @include respond-to(mobile) {
                padding-bottom: 43px;
            }
        }

        &._active {
            .circle {
                background-color: $active;
                color: #fff;
            }
        }

        &._horizontal {
            flex-direction: column;
            min-width: 6.9rem;
            min-height: auto;

            .progress {
                width: auto;
                height: 3.2rem;
            }

            .line {
                top: 50%;
                left: 0;
                width: 100%;
                height: 2px;
                transform: translateY(-50%);
            }
        }
    }

    .progress {
        position: relative;
        flex-shrink: 0;
        width: 3.2rem;
    }

    .line {
        position: absolute;
        top: 0;
        left: 50%;
        width: 2px;
        height: 100%;
        background-color: $secondary;
        transform: translateX(-50%);
    }

    .lineFill {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 0;
        background-color: $primary-100;
        transition: height linear;
    }

    .circle {
        @include text(l4-regular);

        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 3.2rem;
        height: 3.2rem;
        border-radius: 100%;
        background-color: $secondary;
        text-align: center;
        color: $base-600;
        transition: background-color .1s linear, color linear;
    }

    .content {
        flex-grow: 1;
        min-width: 0; // https://stackoverflow.com/a/56122154/15028400
        margin-left: 4.8rem;

        @include respond-to(tablet) {
            margin-left: 2rem;
        }
    }
</style>
