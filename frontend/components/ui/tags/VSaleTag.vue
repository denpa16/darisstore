<script setup lang="ts">
// #region Imports
// Types
import type { VSaleTagProps } from './types.ts';
// #endregion

// #region Props
const {
    to,
    href,
    size = 'small',
    color = 'green-stroke',
    label = '+5%',
    text,
    tag = 'div',
    saleLabel = 'Акция',
    isGarland = false,
} = defineProps<VSaleTagProps>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${color}`]]: color,
        [$style[`_${size}`]]: size,
        [$style._garland]: isGarland,
    },
]);
// #endregion
</script>

<template>
    <component
        :is="tag"
        :class="[$style.VSaleTag, classList]"
        :to="tag === 'NuxtLink' ? to : undefined"
        :href="tag === 'a' ? href : undefined"
        v-bind="$attrs"
    >
        <div v-if="saleLabel" :class="$style.saleShild">
            {{ saleLabel }}
        </div>

        <div
            v-if="label"
            :class="$style.label"
        >
            {{ label }}
        </div>

        <div
            v-if="text"
            :class="$style.text"
        >
            {{ text }}
        </div>
    </component>
</template>

<style lang="scss" module>
    .VSaleTag {
        position: relative;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        user-select: none;
        border-radius: 50%;
        color: $base-600;
        transition: $default-transition;

        /* -- Size -- */
        &._large {
            width: 10rem;
            height: 10rem;
            border: 3px solid;

            .label {
                @include text(l2-regular);
            }

            .text {
                @include text(l4);
            }
        }

        &._medium {
            width: 6.4rem;
            height: 6.4rem;
            border: 2px solid;

            .label {
                @include text(l3-regular);
            }

            .text {
                @include text(l5);
            }
        }

        &._small {
            width: 4rem;
            height: 4rem;
            border: 2px solid;

            .label {
                @include text(l4-regular);
            }

            .saleShild {
                top: -1.7rem;
                height: 2rem;
                padding: 0 .4rem;
            }
        }

        /* -- Color -- */
        &._grey {
            background-color: $primary-100;
            color: $base-0;
        }

        &._green-stroke {
            border-color: $additional-success-500;
        }

        &._garland {
            &:after {
                content: "";
                position: absolute;
                top: 0;
                left: 1px;
                width: 100%;
                height: 100%;
                background-image: url("~/assets/svg/round-garland.svg");
                background-repeat: no-repeat;
                background-size: 100% 100%;
                pointer-events: none;
                transform: scale(1.3);
            }
        }
    }

    .saleShild {
        position: absolute;
        top: -2rem;
        left: 50%;
        display: flex;
        align-items: center;
        height: 2.4rem;
        padding: 0 .8rem;
        border-radius: .4rem;
        background-color: $additional-success-500;
        color: $base-0;
        transform: rotate(-8.96deg) translateX(-50%);

        @include text(l4-regular);
    }
</style>
