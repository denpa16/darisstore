<script setup lang="ts">
// #region Imports
import { useHeightAnimation } from '~/composables/animation/useHeightAnimation';
import type { TColor, TTheme } from '@/types/ui/type.ts';
// #endregion

// #region Props

export interface IProps {
    theme?: TTheme;
    color?: Extract<TColor, 'primary'>;
    shadow?: boolean;
}

const props = withDefaults(defineProps<IProps>(), { theme: 'light', color: 'primary' });
// #endregion

// #region Data
const $style = useCssModule();
const isOpen = ref(false);
const instance = getCurrentInstance();
const contentRef = ref<HTMLElement | null>(null);
const vAccordionRegister = inject('vAccordionRegister');
const vAccordionUnregister = inject('vAccordionUnregister');
const vAccordionSetOpen = inject('vAccordionSetOpen');
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._expanded]: isOpen.value,
        [$style[`_${props.theme}`]]: props.theme,
        [$style[`_${props.color}`]]: props.color,
        [$style._shadow]: props.shadow,
    },
]);
// #endregion

// #region Lifecycle
onMounted(() => {
    vAccordionRegister(instance);
});

onUnmounted(() => {
    vAccordionUnregister(instance);
});

defineExpose({
    toggle,
});
// #endregion

// #region Methods
function toggle(value: boolean) {
    if (value !== isOpen.value) {
        isOpen.value = value;
        vAccordionSetOpen(instance, isOpen.value);
    }

    const { animate } = useHeightAnimation({
        element: contentRef.value,
        isActive: isOpen.value,
    });

    animate();
}

// #endregion
</script>

<template>
    <div :class="[$style.VAccordionItem, classList]">
        <div
            :class="$style.header"
            @click="toggle(!isOpen)"
        >
            <slot name="header-content"></slot>

            <slot name="header-icon" :open="isOpen">
                <VIcon
                    :class="$style.icon"
                    name="mock-arrow"
                />
            </slot>
        </div>

        <div
            ref="contentRef"
            :class="$style.contentWrap"
        >
            <div :class="$style.content">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style lang="scss" module>
    .VAccordionItem {
        position: relative;
        transition: background-color $default-transition, color $default-transition;

        &:first-child {
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;

            &:before {
                border-top: 1px solid;
            }
        }

        &:last-child {
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;

            &:before {
                border-bottom: 1px solid;
            }
        }

        &:not(:first-child) {
            &:after {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                left: 0;
                border-top: 1px solid;
                transition: border-color $default-transition;
            }
        }

        &:before {
            content: "";
            position: absolute;
            inset: 0 0 0 0;
            border-radius: inherit;
            border-right: 1px solid;
            border-left: 1px solid;
        }

        &._expanded {
            & .icon {
                transform: rotateZ(-90deg);
            }
        }

        &._shadow {
            &:before {
                z-index: -1;
                border: none;
                box-shadow: 0 3px 1px -2px rgb(0 0 0 / 20%), 0 2px 2px 0 rgb(0 0 0 / 10%), 0 1px 5px 0 rgb(0 0 0 / 12%);
            }
        }

        /* Themes */
        &._light {
            &._primary {
                background-color: $base-0;
                color: $base-600;

                &:before {
                    border-color: rgba($base-600, .12);
                }

                &:not(:first-child) {
                    &:after {
                        border-color: rgba($base-600, .12);
                    }
                }
            }
        }

        &._dark {
            &._primary {
                background: $base-600;
                color: $base-0;

                &:before {
                    border-color: rgba($base-0, .12);
                }

                &:not(:first-child) {
                    &:after {
                        border-color: rgba($base-0, .12);
                    }
                }
            }
        }
    }

    .header {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.6rem 2.4rem;
        border-top-left-radius: inherit;
        border-top-right-radius: inherit;
        cursor: pointer;
        user-select: none;
    }

    .contentWrap {
        overflow: hidden;
        height: 0;
    }

    .content {
        padding: 0 2.4rem 1.6rem;
    }

    .icon {
        flex-shrink: 0;
        width: 1.6rem;
        height: 1.6rem;
        margin-left: 1.6rem;
        transform: rotateZ(90deg);
        transition: transform $default-transition;
    }
</style>
