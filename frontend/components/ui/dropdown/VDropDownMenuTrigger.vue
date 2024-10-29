<script setup lang="ts">
// #region Imports
// Vue
import { computed } from 'vue';

// Types
import type { DropDownMenuTriggerProps } from './types.ts';
import type { VIconProps } from '~/components/ui/icon/types.ts';
// #endregion

// #region Props
const props = withDefaults(defineProps<DropDownMenuTriggerProps>(), {
    theme: 'light',
    color: 'primary',
    label: 'Label',
});
// #endregion


// #region Constant
const iconAttr: VIconProps = {
    name: 'arrow-down',
    size: 'medium',
};
// #endregion

const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.theme,
        [$style._active]: props.isActive,
        [$style._valid]: props.isValid,
        [$style._disabled]: props.disabled,
    },
]);
// #endregion
</script>

<template>
    <div :class="[$style.VDropDownMenuTrigger, classList]">
        <span :class="$style.label">{{ label }}</span>
        <VIcon
            :class="$style.icon"
            v-bind="iconAttr"
        />
    </div>
</template>

<style lang="scss" module>
    .VDropDownMenuTrigger {
        display: flex;
        align-items: center;
        gap: .8rem;
        width: fit-content;
        height: 4.8rem;
        padding: 0 2rem 0 1.6rem;
        border-radius: 100px;
        border: 1px solid transparent;
        transition: background-color $default-transition, border-color $default-transition;
        cursor: pointer;

        &._active {
            .icon {
                transform: rotate(180deg);
            }
        }

        &._light {
            &._primary {
                background-color: rgba($base-600, .06);
                color: $base-600;

                &._active {
                    border: 1px solid $base-600;
                }

                &._valid {
                    border: 1px solid $base-400;
                }

                &._disabled {
                    color: $base-400;
                    cursor: not-allowed;
                }

                @include hover {
                    &:not(._disabled) {
                        &:not(._active) {
                            background-color: $base-200;
                        }
                    }
                }
            }
        }

        &._dark {
            &._primary {
                background-color: rgba($base-0, .1);
                color: $base-0;

                &._active {
                    border: 1px solid $base-0;
                }

                &._valid {
                    border: 1px solid $opacity-white-40;
                }

                &._disabled {
                    color: rgba($base-0, .4);
                    cursor: not-allowed;
                }

                @include hover {
                    &:not(._disabled) {
                        &:not(._active) {
                            background-color: $base-0;
                            color: $base-600;
                        }
                    }
                }
            }
        }
    }

    .label {
        @include text(l3-regular);
    }

    .icon {
        transition: transform $default-transition;
    }
</style>
