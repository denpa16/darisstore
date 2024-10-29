<script setup
        lang="ts"
>
// #region Imports
// More test
import type { VTabProps } from './types.ts';
// #endregion

// #region Props
const {
    active,
    disabled,
    tag = 'li',
    slider = false,
    theme = 'light',
    size = 'medium',
    close = false,
    extraPad,
} = defineProps<VTabProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'tab-enter': [e: MouseEvent],
    'tab-leave': [e: MouseEvent],
    'tab-info-enter': [e: MouseEvent],
    'tab-info-leave': [e: MouseEvent],
}>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._active]: active,
        [$style._disabled]: disabled,
        [$style._close]: close,
        [$style[`_${size}`]]: size,
        [$style[`_${theme}`]]: theme,
        [$style._slider]: slider,
        [$style._extraPad]: extraPad,
    },
]);
// #endregion
</script>

<template>
    <component
        :is="tag"
        :class="[$style.VTab, classList]"
        @mouseenter="emit('tab-enter', $event)"
        @mouseleave="emit('tab-leave', $event)"
    >
        <slot></slot>
    </component>
</template>

<style lang="scss"
       module
>
    .VTab {
        position: relative;
        display: flex;
        align-items: center;
        gap: .8rem;
        white-space: nowrap;
        line-height: 1.3;
        transition: color $default-transition;
        cursor: pointer;
        user-select: none;

        @include respond-to(mobile) {
            font-size: 1.4rem;
        }

        .icon {
            @include respond-to(mobile) {
                pointer-events: none;
            }
        }

        @include hover {
            color: $base-400;
        }

        /* Sizes */
        &._small {
            @include text(l2-regular);

            padding: 2.6rem 0;

            &._close {
                @include text(l4-regular);

                min-width: 4.8rem;
                height: 4rem;
                padding: 0 1.6rem;
                font-size: 1.4rem;
                font-weight: 500;

                &._extraPad {
                    padding: 0 1.6rem;
                }
            }
        }

        &._medium {
            @include text(l1-regular);

            padding: 2.6rem 0;

            &._close {
                min-width: 4.8rem;
                height: 4rem;
                padding: 0 2rem;
                font-size: 1.4rem;
            }
        }

        /* Themes */
        &._light {
            background-color: $base-0;
            color: $base-600;

            &:after {
                background-color: $base-600;
            }

            @include hover {
                color: $base-400;
            }

            &._active {
                color: $base-600;

                @include hover {
                    background-color: $base-400;
                }

                &:after {
                    background-color: $base-600;
                }

                .icon {
                    color: $base-0;
                }
            }

            &._disabled {
                &:not(._active) {
                    color: $base-400;
                }
            }

            &._close {
                border: 1px solid $base-400;

                &._active {
                    border-color: $base-600;
                    background-color: $base-600;
                    color: $base-0;
                }

                &._disabled {
                    &:not(._active) {
                        border-color: $base-400;
                        background-color: transparent;
                        color: $base-400;
                    }
                }
            }

            &._slider {
                &._active,
                &._close {
                    border: none;
                    background-color: transparent;
                }

                &._close {
                    @include hover {
                        background-color: $base-200;
                    }

                    &._active {
                        background-color: transparent;
                        color: $base-600;
                    }
                }
            }

            .icon {
                color: $base-400;
            }
        }

        /* Modificators */
        &._active {
            &:after {
                transform: scaleX(1);
            }
        }

        &._disabled {
            &:not(._active) {
                cursor: not-allowed;

                &:after {
                    transform: scaleX(0);
                }
            }
        }

        &._close {
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: .8rem;
            transition: color $default-transition, border-color $default-transition, background-color $default-transition;

            &:after {
                display: none;
            }
        }

        &:after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: .2rem;
            transform: scaleX(0);
            transform-origin: left center;
            transition: transform $default-transition;
            pointer-events: none;
        }

        &._slider {
            &._active {
                &:after {
                    display: none;
                }
            }
        }
    }
</style>
