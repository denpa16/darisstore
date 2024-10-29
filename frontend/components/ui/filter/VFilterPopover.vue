<script setup
        lang="ts"
>
// #region Imports
import { onClickOutside } from '@vueuse/core';
import type { VFilterPopoverProps } from '~/components/ui/filter/types.ts';
// #endregion

// #region Props
const {
    label,
    active,
    position = 'center',
    popWidth = '38rem',
    hasLeftActive,
    hasRightActive,
    hasLeftInteracting,
    hasRightInteracting,
    theme = 'light',
} = defineProps<VFilterPopoverProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'open': [],
    'close': [],
    'opener-mouseenter': [],
    'opener-mouseleave': [],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const isOpen = ref(false);
const activatorRef = ref<HTMLElement | null>(null);
// #endregion

// #region Computed
const classList = computed(() => [

    `${$style[`_align-${position}`]}`,
    {
        [$style._open]: isOpen.value,
        [$style._active]: active,
        [$style._hasLeftActive]: hasLeftActive,
        [$style._hasRightActive]: hasRightActive,
        [$style._hasLeftInteracting]: hasLeftInteracting,
        [$style._hasRightInteracting]: hasRightInteracting,
        [$style[`_${theme}`]]: theme,
    },
]);
// #endregion

// #region Lifecycle
onClickOutside(activatorRef, onOutsideClick);
// #endregion

// #region Methods
function onOutsideClick() {
    setOpen(false);
}

function setOpen(val: boolean) {
    if (val) {
        emit('open');
    } else {
        emit('close');
    }
    isOpen.value = val;
}

// #endregion
</script>

<template>
    <div
        ref="activatorRef"
        :class="[$style.VFilterPopover, ...classList]"
    >
        <div
            :class="$style.opener"
            @click="setOpen(!isOpen)"
            @mouseenter="emit('opener-mouseenter')"
            @mouseleave="emit('opener-mouseleave')"
        >
            <slot name="opener">
                <span :class="$style.label">
                    <span
                        :class="$style.labelText"
                        v-html="label"
                    ></span>
                    <VIcon
                        name="mock-arrow-down-s"
                        :class="$style.labelSvg"
                    />
                </span>
            </slot>
        </div>

        <div
            :style="{width: popWidth}"
            :class="$style.content"
        >
            <div
                v-if="$slots.nonscroll"
                :class="$style.contentNonscroll"
            >
                <slot name="nonscroll"></slot>
            </div>
            <VScrollBox
                v-if="$slots.default"
                :class="$style.contentScroll"
                resizable
                skip-offset
                has-margin
            >
                <slot></slot>
            </VScrollBox>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    .VFilterPopover {
        position: relative;
        flex-grow: 1;
        height: 100%;
        border-radius: 50px;
        border: 1px solid transparent;
        transition: $default-transition;

        &:last-child,
        &._open,
        &._hasRightInteracting,
        &._hasRightActive:not(._active),
        &._active:not(._hasRightActive) {
            .opener {
                &:after {
                    opacity: 0;
                }
            }
        }

        &._active {
            &._hasRightActive {
                border-bottom-right-radius: 0;
                border-top-right-radius: 0;
            }

            &._hasLeftActive {
                border-top-left-radius: 0;
                border-bottom-left-radius: 0;
            }
        }

        &._open {
            .labelSvg {
                transform: rotate(180deg);
            }

            .content {
                opacity: 1;
                pointer-events: all;
            }
        }

        &._align-left {
            .content {
                left: -1px;
            }
        }

        &._align-right {
            .content {
                right: -1px;
            }
        }

        &._align-center {
            .content {
                left: 50%;
                transform: translateX(-50%);
            }
        }

        &:not(._open) {
            .opener {
                @include hover {
                    &:hover {
                        background: $base-200;
                    }
                }
            }
        }

        &._light {
            &._active {
                border-color: $base-400;

                &._hasRightActive {
                    &:not(._open) {
                        border-right-color: transparent;
                    }
                }

                &._hasLeftActive {
                    &:not(._open) {
                        border-left-color: transparent;
                    }
                }
            }

            &._open {
                border-color: $base-600;
            }

            .opener {
                &:after {
                    background-color: $base-400;
                }

                @include hover {
                    &:hover {
                        background: $base-200;
                    }
                }
            }

            .label {
                color: $base-600;
            }
        }

        &._dark {
            &._active {
                border-color: $base-0;

                &._hasRightActive {
                    &:not(._open) {
                        border-right-color: transparent;
                    }
                }

                &._hasLeftActive {
                    &:not(._open) {
                        border-left-color: transparent;
                    }
                }
            }

            &._open {
                border-color: $base-0;
            }

            .opener {
                &:after {
                    background-color: $base-400;
                }

                @include hover {
                    &:hover {
                        background: $base-200;

                        .label {
                            color: $base-600;
                        }
                    }
                }
            }

            .label {
                color: $base-0;
            }
        }
    }

    .opener {
        position: relative;
        width: 100%;
        height: 100%;
        border-radius: 50px;
        transition: $default-transition;
        cursor: pointer;

        &:after {
            content: "";
            position: absolute;
            top: 50%;
            right: 0;
            width: .1rem;
            height: 2rem;
            opacity: 1;
            transform: translateY(-50%);
            transition: $default-transition;
        }

        @include hover {
            &:hover {
                &:after {
                    opacity: 0;
                }

                .label {
                    z-index: 1;
                }
            }
        }
    }

    .label {
        position: relative;
        display: flex;
        align-items: center;
        height: 100%;
        padding: 0 2rem;
        border-radius: inherit;
        background: transparent;
        white-space: nowrap;
        font-size: 1.4rem;
        font-weight: bold;
        line-height: 130%;
        transition: $default-transition;
    }

    .labelSvg {
        flex-shrink: 0;
        margin-left: 16px;
        transition: transform $default-transition;
    }

    .labelText {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .content {
        position: absolute;
        top: calc(100% + 8px);
        z-index: 3;
        border-radius: 1.2rem;
        background: $base-0;
        box-shadow: 0 4px 38px 0 rgb(21 22 24 / 8%);
        opacity: 0;
        pointer-events: none;
        transition: $default-transition;
    }

    .contentScroll {
        max-height: 60vh;
    }
</style>
