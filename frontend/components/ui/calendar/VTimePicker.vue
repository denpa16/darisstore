<script setup lang="ts">
// #region Imports
import type { PropsTimePicker } from './types.ts';
// #endregion

// #region Props
const {
    label = 'Выберите удобное время:',
    modelValue,
    availableTime,
    disabled,
    theme = 'light',
} = defineProps<PropsTimePicker>();
// #endregion

// #region Emits
const emit = defineEmits(['update:modelValue']);
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style._disabled]: disabled,
    },
]);
// #endregion
</script>

<template>
    <div :class="[$style.VTimePicker, classList]">
        <div
            :class="$style.label"
            v-html="label"
        >
        </div>

        <div
            v-if="availableTime"
            :class="$style.list"
        >
            <div
                v-for="(item, idx) in availableTime"
                :key="`item_${item.value}_${idx}`"
                :class="[$style.item, {[$style._selected]: item.value === modelValue}]"
                @click="emit('update:modelValue', item.value)"
            >
                {{ item.label }}
            </div>
        </div>
    </div>
</template>

<style module lang="scss">
    .VTimePicker {
        position: relative;

        /* Colors */
        &._light {
            .label {
                color: $base-500;
            }

            .item {
                background-color: $base-100;
                color: $base-600;

                &._disabled {
                    color: $base-400;
                }

                &._selected {
                    background-color: $base-600;
                    color: $base-0;
                }

                @include hover {
                    &:hover {
                        &:not(._selected, ._disabled) {
                            background-color: $base-200;
                        }
                    }
                }
            }

            &._disabled {
                opacity: .5;
            }
        }

        &._disabled {
            pointer-events: none;
        }
    }

    .label {
        font-size: 1.2rem;
        line-height: 130%;
    }

    .list {
        display: flex;
        gap: .2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
    }

    .item {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 6rem;
        height: 2.8rem;
        border-radius: .4rem;
        font-size: 1.2rem;
        line-height: 130%;
        transition: $default-transition;
        cursor: pointer;
        user-select: none;

        &._disabled {
            cursor: not-allowed;
        }
    }
</style>
