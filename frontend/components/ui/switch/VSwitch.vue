<script setup lang="ts">
/**
 * Позволяет пользователю выбрать одно из двух значений, для передачи в форму.
 *
 * @version 1.0.1
 * @displayName VSwitch
 */

// #region Imports
import type { Props } from './types.ts';
import { ColorsEnum, SizeEnum } from '@/types/ui/type.ts';
// #endregion

// #region Props
const props = withDefaults(defineProps<Props>(), {
    name: '',
    size: SizeEnum.medium,
    color: ColorsEnum.primary,
    trueValue: true,
    falseInfo: '',
    trueInfo: '',
});
// #endregion

// #region Emits
const emit = defineEmits<{
    change: [value: (boolean | Record<string, boolean>)],
    'update:modelValue': [value: boolean],
}>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const active = computed(() => Array.isArray(props.modelValue) ? props.modelValue.includes(props.trueValue) : props.modelValue === props.trueValue);

const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.theme,
        [$style[`_${props.color}`]]: props.color,
        [$style[`_${props.size}`]]: props.size,
        [$style._disabled]: props.disabled,
        [$style._active]: active.value,
        [$style._notChecked]: !active.value,
    },
]);
// #endregion

// #region Methods
function onChange(e: Event) {
    nextTick(() => {
        /**
         * Возвращает новое значение в родительский компонент.
         @param {String|Boolean} value Новое значение
         */
        emit('update:modelValue', (e.target as HTMLInputElement).checked);
        emit('change', name ? { [name]: (e.target as HTMLInputElement).checked } : (e.target as HTMLInputElement).checked);
    });
}

// #endregion
</script>

<template>
    <label
        :class="[$style.VSwitch, classList]"
        role="switch"
        :aria-checked="active"
        :aria-disabled="disabled"
        :data-test-id="name"
        :tabindex="disabled ? false : 0"
    >

        <input
            :checked="active"
            :class="$style.input"
            :name="name"
            :disabled="disabled"
            :true-value="trueValue"
            :false-value="falseValue"
            aria-hidden="true"
            type="checkbox"
            tabindex="-1"
            @change="onChange"
        >

        <span
            v-if="$slots.falseLabel"
            :class="[$style.label, $style._left]"
        >
            <!-- @slot Не всегда соответствует передаваемой данной в форме -->
            <slot name="falseLabel"></slot>
            <VTooltip
                v-if="falseInfo"
                :text="falseInfo"
                :class="$style.icon"
            >
                <template #activator>
                    <VIcon
                        name="information"
                        :size="size === 'large' ? 'sLarge' : 'medium'"
                    />
                </template>
            </VTooltip>
        </span>

        <div :class="$style.core"></div>

        <span
            v-if="$slots.trueLabel"
            :class="[$style.label, $style._right]"
        >
            <!-- @slot Не всегда соответствует передаваемой данной в форме -->
            <slot name="trueLabel"></slot>
            <VTooltip
                v-if="trueInfo"
                :text="trueInfo"
                :class="$style.icon"
            >
                <template #activator>
                    <VIcon
                        name="information"
                        :size="size === 'large' ? 'sLarge' : 'medium'"
                    />
                </template>
            </VTooltip>
        </span>
    </label>
</template>

<style lang="scss" module>
    .VSwitch {
        display: inline-flex;
        align-items: center;
        outline: none;
        transition: opacity $default-transition;
        cursor: pointer;
        user-select: none;

        /* Themes */
        &._light {
            &._primary {
                @include hover {
                    .core {
                        background-color: $base-500;
                    }
                }

                .core {
                    background-color: $base-200;
                }

                .label {
                    color: $base-600;

                    &._left {
                        color: $base-400;
                    }
                }

                .icon {
                    color: $base-400;
                }

                &._active {
                    .core {
                        background-color: $primary-900;
                    }

                    @include hover {
                        .core {
                            background-color: $primary-600;
                        }
                    }

                    .label {
                        &._left {
                            color: $base-400;
                        }

                        &._right {
                            color: $base-600;
                        }
                    }
                }

                &._disabled {
                    .core {
                        background-color: $base-100;
                    }

                    .label {
                        &._left,
                        &._right {
                            color: $base-400;
                        }
                    }

                    .icon {
                        color: $base-400;
                    }

                    &._active {
                        .core {
                            background-color: $primary-600;
                        }
                    }
                }
            }
        }

        /* Sizes */
        &._medium {
            .label {
                font-size: 1.6rem;

                &._left {
                    margin-right: 1.2rem;
                }

                &._right {
                    margin-left: 1.2rem;
                }
            }

            .core {
                width: 3.2rem;
                height: 2rem;

                &:after {
                    width: 1.6rem;
                    height: 1.6rem;
                }
            }

            .icon {
                width: 1.6rem;
                height: 1.6rem;
                margin-left: .8rem;
            }

            &._active {
                .core {
                    &:after {
                        left: calc(100% - 1.8rem);
                    }
                }
            }
        }

        /* Modificators */
        &._disabled {
            pointer-events: none;
        }
    }

    .input {
        display: none;
    }

    .label {
        display: flex;
        align-items: center;
        line-height: 1;
        transition: color $default-transition;
    }

    .core {
        position: relative;
        flex-shrink: 0;
        border-radius: 10rem;
        transition: background-color $default-transition;

        &:after {
            content: "";
            position: absolute;
            top: 50%;
            left: .2rem;
            border-radius: 50%;
            background-color: $base-0;
            transform: translateY(-50%);
            transition: left $default-transition;
            box-shadow: 0 .1rem .4rem rgb(0 0 0 / 25%);
            will-change: left;
        }
    }

    .icon {
        margin-left: .8rem;
    }
</style>
