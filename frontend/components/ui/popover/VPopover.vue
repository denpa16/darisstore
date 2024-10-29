<script setup lang="ts">
/**
 * @version 1.0.0
 * @displayName VPopover
 */

// #region Imports
// Vue
import { onClickOutside } from '@vueuse/core';

// Types
import type { Props } from './types.ts';
// #endregion

// #region Props
const {
    direction = 'bottom',
    width = '100%',
    height = '100%',
    background = '',
    sharp = false,
    round = false,
    shadow = false,
} = defineProps<Props>();
// #endregion

// #region Emits
const emit = defineEmits<{
    close: [],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const isContentVisible = ref(false);
const contentRef = ref<HTMLElement | null>(null);
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${direction}`]]: direction,
        [$style._visible]: isContentVisible.value,
        [$style._sharp]: sharp,
        [$style._round]: round,
        [$style._shadow]: shadow,
    },
]);
// #endregion

// #region Lifecycle
onClickOutside(contentRef, () => onClick());
// #endregion

// #region Methods
function onClick() {
    isContentVisible.value = false;

    setTimeout(() => {
        emit('close');
    }, 300);
}

// #endregion
</script>

<template>
    <transition
        name="overlay-appear"
        appear
        @after-enter="isContentVisible = true"
    >
        <div :class="$style.overlay">
            <div
                ref="contentRef"
                :class="[$style.content, classList]"
                :style="{
                    width: width,
                    height: height,
                    background: background,
                }"
            >
                <div :class="$style.close">
                    <VButton
                        size="small"
                        @click="onClick"
                    >
                        <VIcon
                            :class="$style.closeIcon"
                            name="mock-close"
                            size="custom"
                        />
                    </VButton>
                </div>

                <slot></slot>
            </div>
        </div>
    </transition>
</template>


<style lang="scss" module>
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 99;
        overflow: hidden;
        width: 100%;
        height: 100%;
        background-color: rgb(0 0 0 / 30%);
        transition: .5s all ease;
    }

    .content {
        position: relative;
        transition: transform .3s linear;

        &._top {
            transform: translate3d(0, -100%, 0);
        }

        &._right {
            transform: translate3d(100%, 0, 0);
        }

        &._bottom {
            transform: translate3d(0, 100%, 0);
        }

        &._left {
            transform: translate3d(-100%, 0, 0);
        }

        &._visible {
            transform: translate3d(0, 0, 0);
        }

        &._sharp {
            border-radius: 0;
        }

        &._round {
            border-radius: 8px;
        }

        &._shadow {
            box-shadow: 0 4px 12px rgb(0 0 0 / 5%);
        }
    }

    .close {
        position: absolute;
        top: 16px;
        right: 16px;
        display: inline-block;
    }

    .closeIcon {
        width: 24px;
        height: 24px;
    }
</style>
