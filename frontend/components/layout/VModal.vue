<script setup
        lang="ts"
>
// #region Imports
import type { CSSProperties } from 'vue';
import { disablePageScroll, enablePageScroll } from 'scroll-lock/src/scroll-lock';
// #endregion

// #region Data
const $style = useCssModule();

const emit = defineEmits<{
    'update:modelValue': [value: boolean],
}>();

export interface Props {
    position?: 'center' | 'left' | 'right',
    align?: 'center' | 'top' | 'bottom',
    animation?: 'slide_left' | 'slide_right' | 'scale' | 'slide_bottom',
    noOverlay?: boolean,
    modelValue?: boolean,
    overlayColor?: string,
}

const props = withDefaults(defineProps<Props>(), {
    position: 'center',
    align: 'center',
    animation: 'slide_left',
    noOverlay: false,
    modelValue: false,
    overlayColor: '',
});

const overlayStyles = computed<CSSProperties>(() => {
    const styles: CSSProperties = {};

    if (props.overlayColor) {
        styles['--overlay-color'] = props.overlayColor;
    }

    return styles;
});

// #endregion

// #region Computed
const classList = computed(() => [
    $style[`position_${props?.position}`],
    $style[`animation_${props?.animation}`],
    $style[`align_${props?.align}`],
]);
// #endregion

// #region Watch
const modalRef = ref<HTMLElement | null>(null);

// Устанавливаем фокус на модалку, для отслеживания нажатия на кнопку esc на клаве, для закрытия
// Если удалить tabindex у элемента, то фокус не будет устанавливаться
watch(() => props.modelValue, () => {
    if (props.modelValue) {
        nextTick(() => {
            modalRef.value?.focus();
        });
    }
});
// #endregion

// #region Methods
function beforeEnter() {
    disablePageScroll();
}

function afterLeave() {
    enablePageScroll();
}

function handleClose() {
    emit('update:modelValue', false);
}
// #endregion
</script>

<template>
    <VTeleport
        to="#app"
    >
        <transition
            :duration="500"
            name="modal"
            @before-enter="beforeEnter"
            @after-leave="afterLeave"
        >
            <div
                v-if="modelValue"
                ref="modalRef"
                :class="[$style.VModal, classList, 'v-modal']"
                tabindex="0"
                @keyup.esc="handleClose"
            >
                <div
                    v-bind="$attrs"
                    :class="$style.container"
                    data-scroll-lock-scrollable
                >
                    <slot/>
                </div>

                <div
                    v-if="!props.noOverlay"
                    :class="$style.overlay"
                    :style="overlayStyles"
                    @mousedown.self="handleClose"
                />
            </div>
        </transition>
    </VTeleport>
</template>

<style lang="scss" module>
    :root {
        --overlay-color: rgb(0 0 0 / 50%);
    }

    .VModal {
        position: fixed;
        inset: 0;
        z-index: 1000;
        outline: none;

        /* position */
        &.position {
            &_left {
                .container {
                    justify-content: flex-start;
                }
            }

            &_right {
                .container {
                    justify-content: flex-end;
                }
            }

            &_center {
                .container {
                    justify-content: center;
                }
            }
        }

        /* align */
        &.align {
            &_top {
                .container {
                    align-items: flex-start;
                }
            }

            &_bottom {
                .container {
                    align-items: flex-end;
                }
            }

            &_center {
                .container {
                    align-items: center;
                }
            }
        }


        &:global(.modal-enter-active),
        &:global(.modal-leave-to) {
            .overlay {
                opacity: 1;
                transition: opacity .3s ease;
            }

            .container,
            .close {
                opacity: 1;
                transform: translate3d(0, 0, 0);
                transition: opacity .2s ease .3s, transform .2s ease .3s;
            }
        }

        &:global(.modal-enter-from),
        &:global(.modal-leave-active) {
            .overlay {
                opacity: 0;
                transition: opacity .3s ease .2s;
            }

            .container,
            .close {
                opacity: 0;
                transform: translate3d(100%, 0, 0);
                transition: opacity .2s ease, transform .2s ease;

                @include respond-to(tablet) {
                    transform: translate3d(0, 100%, 0);
                }
            }
        }

        /* animation */
        &.animation {
            &_slide_left {
                &:global(.modal-enter-from),
                &:global(.modal-leave-active) {
                    .container {
                        transform: translate3d(-100%, 0, 0);
                    }
                }
            }

            &_slide_right {
                &:global(.modal-enter-from),
                &:global(.modal-active) {
                    .container {
                        transform: translate3d(100%, 0, 0);
                    }
                }
            }

            &_slide_bottom {
                &:global(.modal-enter-from),
                &:global(.modal-leave-active) {
                    .container {
                        transform: translate3d(0, 100%, 0);
                    }
                }
            }

            &_scale {
                .container {
                    transform: scale(1);
                }

                &:global(.modal-enter-from),
                &:global(.modal-leave-active) {
                    .container {
                        transform: scale(.5);
                    }
                }
            }
        }

        .overlay {
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            z-index: 1;
            background-color: var(--overlay-color);
        }

        .container {
            position: absolute;
            z-index: 2;
            overflow-y: auto;
            display: flex;
            width: 100%;
            height: 100%;
            pointer-events: none;

            & > * {
                pointer-events: auto;
            }
        }
    }
</style>
