<script setup
        lang="ts"
>/**
 * Кастомная альтернатива тега button в стандартном html<br>
 * На проектах, обычно, имеет несколько цветов, форм и состояний.<br><br>
 * Область применения: ссылка, изменения состояния, вызов методов.
 *
 * @displayName VChecbox
 */
import {
    ColorsEnum,
    SizeEnum,
    type TColor,
    ThemeEnum,
    type TSize,
    type TTheme,
} from '@/types/ui/type.ts';

// #region Interfaces
interface ICheckboxProps {
    name?: string | undefined;
    modelValue?: Array<string | boolean> | string | boolean;
    trueValue?: string | boolean;
    falseValue?: string | boolean;
    size?: Extract<TSize, 'medium'>;
    theme?: Extract<TTheme, 'light'>;
    color?: Extract<TColor, 'primary'>;
    radio?: boolean,
    disabled?: boolean,
    label?: string,
    msg?: string;
    info?: string;
}

// #endregion

// #region Props
const props = withDefaults(defineProps<ICheckboxProps>(), {
    name: 'checkbox',
    modelValue: false,
    trueValue: true,
    falseValue: false,
    size: SizeEnum.medium,
    theme: ThemeEnum.light,
    color: ColorsEnum.primary,
    label: '',
    msg: '',
    info: '',
});
// #endregion

// #region Emits
const emit = defineEmits<{
    focus: [value: FocusEvent],
    blur: [value: FocusEvent],
    'update:modelValue': [value: boolean],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const labelRef = ref<HTMLElement | null>(null);
const isFocused = ref(false);
// #endregion

// #region Computed
const active = computed(() => {
    if (Array.isArray(props.modelValue)) {
        return props.modelValue.includes(props.trueValue);
    }

    return props.modelValue === props.trueValue;
});

const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.theme,
        [$style[`_${props.color}`]]: props.color,
        [$style[`_${props.size}`]]: props.size,
        [$style._radio]: props.radio,
        [$style._checkbox]: !props.radio,
        [$style._active]: active.value,
        [$style._disabled]: props.disabled,
        [$style._focused]: isFocused.value,
    },
]);
// #endregion

// #region Methods
const onFocus = (e: FocusEvent) => {
    isFocused.value = true;
    emit('focus', e);
};

const onBlur = (e: FocusEvent) => {
    isFocused.value = false;
    emit('blur', e);
};

function onEnter() {
    labelRef.value?.click();
}

function onChange(e: Event) {
    emit('update:modelValue', (e.target as HTMLInputElement).checked);
}

// #endregion
</script>

<template>
    <label
        ref="labelRef"
        :class="[$style.VCheckbox, classList]"
        :data-test-id="name"
    >
        <span :class="$style.input">
            <input
                :checked="active"
                :class="$style.inputNative"
                :disabled="props.disabled"
                :false-value="props.falseValue"
                :name="props.name"
                :true-value="props.trueValue"
                :value="props.trueValue"
                type="checkbox"
                @blur="onBlur"
                @focus="onFocus"
                @keydown.enter.stop.prevent="onEnter"
                @change="onChange"
            >
        </span>

        <span
            :class="$style.label"
            :aria-label="props.label"
        >
            {{ props.label }}
        </span>

        <!-- @slot лейбл-->
        <span
            v-if="$slots?.default"
            :class="[$style.label, $style.slotLabel]"
            :aria-label="props.label"
        >
            <slot></slot>
        </span>

        <span
            v-if="props.info"
            :class="$style.info"
        >
            <VTooltip
                :text="props.info"
                tag="span"
            >
                <template #activator>
                    <VIcon name="information" />
                </template>
            </VTooltip>
        </span>

        <transition name="fade-fast">
            <InputHint
                v-if="props.msg"
                :class="$style.msg"
                absolute
            >
                {{ props.msg }}
            </InputHint>
        </transition>
    </label>
</template>

<style lang="scss"
       module
>
    $primary: $primary-900;
    $base-0-color: $base-0;

    .VCheckbox {
        position: relative;
        display: inline-flex;
        align-items: center;
        user-select: none;
        outline: none;
        cursor: pointer;

        /* Themes */
        &._light {
            &._primary {
                .label {
                    color: $base-900;
                }

                .slotLabel {
                    color: $base-500;
                }

                .input {
                    border: .1rem solid $base-200;
                    color: $base-0-color;
                    transition: border-color $default-transition;
                }

                .info {
                    color: $base-200;
                }

                &._active {
                    .input {
                        border-color: $primary;
                    }

                    &._radio,
                    &._checkbox {
                        .input {
                            background-color: $primary;
                        }
                    }
                }

                &._disabled {
                    .label {
                        color: $base-200;
                    }

                    .input {
                        border-color: $base-200;
                    }

                    &._active {
                        .input {
                            border-color: $primary-600;
                            background-color: $primary-600;
                        }
                    }

                    @include hover {
                        &:hover {
                            .input {
                                border-color: $base-400;
                            }
                        }
                    }
                }

                @include hover {
                    &:not(._disabled, ._active) {
                        &:hover {
                            .input {
                                border-color: $base-400;
                            }
                        }
                    }

                    &._active {
                        &:hover {
                            .input {
                                background-color: $primary-600;
                            }
                        }
                    }
                }
            }
        }

        /* Sizes */
        &._medium {
            .label {
                @include text(l2m);

                margin-left: .8rem;
                line-height: 1;
            }

            .input {
                width: 1.6rem;
                height: 1.6rem;

                &:after {
                    width: 1.2rem;
                    height: 1.2rem;
                }
            }

            .info {
                margin-left: .4rem;
            }

            &._radio {
                .input {
                    width: 1.6rem;
                    height: 1.6rem;

                    &:after {
                        width: .8rem;
                        height: .8rem;
                    }
                }
            }

            .msg {
                left: 3.4rem;
            }
        }

        /* Modificators */
        &._radio {
            .input {
                border-radius: 50%;

                &:after {
                    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10.13 10.13'%3E%3Cpath d='M5.06,10A4.94,4.94,0,1,1,10,5.06,4.94,4.94,0,0,1,5.06,10Z'/%3E%3C/svg%3E");
                    /* stylelint-disable */
                    /* postcss-ignore-line */
                    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10.13 10.13'%3E%3Cpath d='M5.06,10A4.94,4.94,0,1,1,10,5.06,4.94,4.94,0,0,1,5.06,10Z'/%3E%3C/svg%3E");
                    /* stylelint-enable */
                }
            }
        }

        &._checkbox {
            .input {
                border-radius: 0;

                &:after {
                    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 7'%3E%3Cpath d='M3.99987 5.586L8.59587 0.989502L9.30337 1.6965L3.99987 7L0.817871 3.818L1.52487 3.111L3.99987 5.586Z'/%3E%3C/svg%3E");
                    /* stylelint-disable */
                    /* postcss-ignore-line */
                    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 7'%3E%3Cpath d='M3.99987 5.586L8.59587 0.989502L9.30337 1.6965L3.99987 7L0.817871 3.818L1.52487 3.111L3.99987 5.586Z'/%3E%3C/svg%3E");
                    /* stylelint-enable */
                }
            }
        }

        &._disabled {
            cursor: not-allowed;

            .input,
            .info {
                pointer-events: none;
            }
        }

        &._active {
            .input {
                &:after {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                }
            }
        }
    }

    .input {
        position: relative;
        flex-shrink: 0;
        transition: border-color .2s ease, background-color .2s ease, transform .2s ease;

        &:after {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            border-radius: 50%;
            background-color: currentcolor;
            opacity: 0;
            transform: translate(-50%, -50%) scale(0);
            transition: opacity $default-transition, transform $default-transition;
            -webkit-mask-repeat: no-repeat;
            mask-repeat: no-repeat;
            -webkit-mask-position: center;
            mask-position: center;
        }
    }

    .inputNative {
        display: none;
    }

    .label {
        white-space: nowrap;
    }

    .msg {
        display: inline;
        width: auto;
        white-space: nowrap;
    }
</style>
