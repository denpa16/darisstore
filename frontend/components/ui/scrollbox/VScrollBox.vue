<script setup
        lang="ts"
>
// #region Imports
import useScrollBox from '@idaproject/core/composables/ui/useScrollBox';
import type { VScrollBoxProps } from './types';
import { ThemeEnum } from '@/types/ui/type.ts'; // #endregion
// #endregion

// #region Props
const {
    resizable = false,
    skipOffset = false,
    hasMargin = false,
    fade = false,
    theme = ThemeEnum.light,
    width,
    height,
} = defineProps<VScrollBoxProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'on-scroll': [],
    'scroll-end': [value: boolean],
}>();
// #endregion

// #region Data
const contentRef = ref<HTMLElement | null>(null);
const wrapperRef = ref<HTMLElement | null>(null);
const boxRef = ref<HTMLElement | null>(null);
const yRailRef = ref<HTMLElement | null>(null);
const xThumbRef = ref<HTMLElement | null>(null);
const yThumbRef = ref<HTMLElement | null>(null);
const xRailRef = ref<HTMLElement | null>(null);
const placeholderRef = ref<HTMLElement | null>(null);


const {
    dimensions,
    yScrollPosition,
    xScrollPosition,
    isXOverflowing,
    isYOverflowing,
    isFadeMaskTop,
    isFadeMaskBottom,
    onScroll,
    onThumbClick,
    onRailClick,
} = useScrollBox(emit, toRef(() => resizable), contentRef, wrapperRef, boxRef, yRailRef, xThumbRef, yThumbRef, xRailRef, placeholderRef);
// #endregion

const classListMask = computed(() => [{
    _top: isFadeMaskTop.value,
    _bottom: isFadeMaskBottom.value,
    _show: fade && isYOverflowing.value,
}]);
</script>

<template>
    <div
        ref="boxRef"
        :class="['c-scrollbox', $style.VScrollBox, {[$style[`_${theme}`]]: theme, [$style._margin]: hasMargin}]"
        :style="{width: width ? width : undefined, height: height ? height : undefined}"
    >
        <div
            ref="placeholderRef"
            :class="$style.placeholder"
        >
        </div>

        <div
            :class="[$style.fadeMask, classListMask]"
        >
            <div
                ref="wrapperRef"
                :class="['scrollbox-wrapper', $style.wrapper, {[$style._offset]: isYOverflowing && !skipOffset}]"
                @scroll="onScroll"
            >
                <div
                    ref="contentRef"
                    :class="$style.content"
                >
                    <slot></slot>
                </div>
            </div>
        </div>

        <div
            v-if="isYOverflowing"
            ref="yRailRef"
            :class="[$style.scrollbar, $style._vertical]"
            @mousedown="onRailClick($event, 'y')"
        >
            <div
                ref="yThumbRef"
                :class="$style.thumb"
                :style="{height: `${dimensions.yThumbHeight}px`, transform: yScrollPosition}"
                @mousedown="onThumbClick($event, 'y')"
            >
            </div>
        </div>

        <div
            v-if="isXOverflowing"
            ref="xRailRef"
            :class="[$style.scrollbar, $style.horizontal]"
            @mousedown="onRailClick($event, 'x')"
        >
            <div
                ref="xThumbRef"
                :class="$style.thumb"
                :style="{width: `${dimensions.xThumbWidth}px`, transform: xScrollPosition}"
                @mousedown="onThumbClick($event, 'x')"
            >
            </div>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    $thumb-dark-color: $base-200;
    $thumb-light-color: $base-200;
    $scrollbar-color: transporent;

    .VScrollBox {
        position: relative;
        overflow: hidden;

        /* Colors */
        &._light {
            .thumb {
                background-color: $thumb-light-color;
            }

            .fadeMask {
                &:before {
                    background: linear-gradient(to bottom, $primary-100 12%, rgba(255 255 255 / 0%));
                }

                &:after {
                    background: linear-gradient(to top, $primary-100 12%, rgba(255 255 255 / 0%));
                }
            }
        }

        &._margin {
            .wrapper {
                &._offset {
                    padding-right: .8rem;
                }
            }

            .scrollbar {
                right: .4rem;
                bottom: .4rem;

                &._horizontal {
                    left: .4rem;
                }

                &._vertical {
                    top: .4rem;
                }
            }
        }

        .wrapper {
            position: absolute;
            inset: 0 0 0 0;
            z-index: 0;
            box-sizing: border-box;
            overflow: auto;
            width: auto;
            max-width: 100%;
            height: 100%;
            max-height: 100%;
            scrollbar-width: none;
            -ms-overflow-style: none;

            &::-webkit-scrollbar {
                width: 0;
                height: 0;
            }

            &._offset {
                padding-right: .8rem;
            }
        }

        .placeholder {
            width: 100%;
            max-width: 100%;
            max-height: 100%;
            pointer-events: none;
        }

        .fadeMask {
            position: absolute;
            top: 0;
            width: 100%;
            height: 100%;

            &:global {
                &._top {
                    &:before {
                        min-height: 0;
                    }
                }

                &._bottom {
                    &:after {
                        min-height: 0;
                    }
                }

                &._show {
                    &:before,
                    &:after {
                        display: block;
                    }
                }
            }

            &:before,
            &:after {
                content: "";
                position: absolute;
                left: 1px;
                z-index: 2;
                display: none;
                width: calc(100% - 1.2rem);
                min-height: 4rem;
                transition: min-height .2s linear;
                pointer-events: none;
            }

            &:before {
                top: 0;
            }

            &:after {
                bottom: 0;
            }
        }
    }

    .scrollbar {
        position: absolute;
        right: 0;
        bottom: 0;
        z-index: 3;
        overflow: hidden;
        width: .4rem;
        border-radius: 6rem;
        background-color: $scrollbar-color;

        &._horizontal {
            left: 0;

            .thumb {
                bottom: .1rem;
                left: 0;
                height: .4rem;
            }
        }

        &._vertical {
            top: 0;

            .thumb {
                top: 0;
                right: 0;
                width: .4rem;
                transition: opacity $default-transition;
                cursor: pointer;

                @include hover {
                    &:hover {
                        opacity: .7;
                    }
                }
            }
        }

        .thumb {
            position: absolute;
            border-radius: 6rem;
        }
    }
</style>
