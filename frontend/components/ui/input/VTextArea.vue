<script setup lang="ts">
/**
 * Позволяет пользователю ввести данные с помощью клавиатуры.<br>
 *
 * @version 1.0.0
 * @displayName VTextArea
 */

// #region Imports
import type { TextAreaProps } from './types.ts';
// #endregion

// #region Props
const props = withDefaults(defineProps<TextAreaProps>(), {
    size: 'medium',
    theme: 'light',
    color: 'primary',
    modelValue: 'text',
    autocomplete: true,
    label: '',
    placeholder: '',
    msg: '',
});
// #endregion

// #region Emits
const emit = defineEmits<{
    focus: [value: FocusEvent],
    blur: [value: FocusEvent],
    'update:modelValue': [value: string],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const isFocused = ref(false);
const attrs = useAttrs();
// #endregion

// #region Computed
const inputValue = computed(() => props.modelValue);

const attributes = computed(() => {
    const attrsValue = {
        ...attrs,
        disabled: props.disabled,
        ariaLabel: '',
        maxlength: 524288,
        autocomplete: 'on',
    };

    if (props.label) {
        attrsValue.ariaLabel = props.label;
    }

    if (!props.autocomplete) {
        attrsValue.autocomplete = 'off';
    }

    return attrsValue;
});

const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.theme,
        [$style[`_${props.color}`]]: props.color,
        [$style[`_${props.size}`]]: props.size,
        [$style._focused]: isFocused.value,
        [$style._disabled]: props.disabled,
        [$style._error]: props.error,
    },
]);

const labelString = computed(() => props.required ? props.label + '<span>*</span>' : props.label);
// #endregion

// #region Lifecycle

// #endregion

// #region Methods
const onFocus = (e: FocusEvent) => {
    isFocused.value = true;
    emit('focus', e);
};

/**
 * Метод, который обрабатывает событие blur на инпуте
 * @public
 */
const onBlur = (e: FocusEvent) => {
    isFocused.value = false;
    emit('blur', e);
};

/**
 * Эмитит новые значения в родительский компонент.
 * Используется для валидации.
 * @returns {String} e.target.value Введёный текст
 * @public
 */
const onInput = (e: Event) => {
    emit('update:modelValue', (e.target as HTMLInputElement).value);
};
// #endregion
</script>

<template>
    <div :class="[$style.VTextArea, classList]">
        <div
            v-if="label"
            :class="$style.label"
            v-html="labelString"
        >
        </div>
        <div :class="$style.wrapper">
            <textarea
                v-bind="attributes"
                :aria-label="label"
                :class="$style.native"
                :tabindex="0"
                :value="inputValue"
                :placeholder="placeholder"
                :data-test-id="name"
                @blur="onBlur"
                @focus="onFocus"
                @input="onInput"
            ></textarea>
        </div>

        <transition name="fade-fast">
            <InputHint
                v-if="msg"
                :theme="error ? 'alert' : theme"
                :disabled="disabled"
            >
                {{ msg }}
            </InputHint>
        </transition>
    </div>
</template>

<style lang="scss" module>
    .VTextArea {
        position: relative;
        width: 100%;

        /* Sizes */
        &._medium {
            .label {
                @include text(l3);
            }

            .wrapper {
                width: 100%;
                height: 100%;
                min-height: 5rem;
                margin-top: 1.2rem;
                padding: 1.6rem;
                border: 1px solid;
                transition: border-color $default-transition;
            }

            .native {
                @include text(t2);

                width: 100%;
                height: 100%;
                padding: 0 1rem;
            }
        }

        /* Colors */
        &._light {
            &._primary {
                .label {
                    color: $base-600;

                    & > span {
                        color: $primary-900;
                    }
                }

                .wrapper {
                    border-color: $base-200;
                }

                &:not(._disabled) {
                    .wrapper {
                        @include hover {
                            border-color: $base-400;
                        }
                    }
                }

                ::placeholder {
                    color: $base-500;
                }

                &._focused {
                    .wrapper {
                        border-color: $base-400;

                        @include hover {
                            &:hover {
                                border-color: $base-600;
                            }
                        }
                    }
                }

                &._error {
                    .wrapper {
                        border-color: $primary-900;

                        @include hover {
                            &:hover {
                                border-color: $primary-900;
                            }
                        }
                    }
                }
            }
        }

        /* Mods */
        &._disabled {
            cursor: not-allowed;
            user-select: none;

            .label {
                pointer-events: none;
            }

            .wrapper {
                border-color: $base-200;
            }

            ::placeholder {
                color: $base-200;
            }

            textarea {
                pointer-events: none;
            }
        }

        textarea {
            resize: vertical;
        }

        textarea::-webkit-scrollbar {
            position: absolute;
            left: 0;
            width: .4rem;
            margin: 4rem;
            padding: 4rem;
        }

        textarea::-webkit-scrollbar-track {
            height: 80%;
            border-radius: 6rem;
            -webkit-box-shadow: none;
        }

        textarea::-webkit-scrollbar-thumb {
            border-radius: 6rem;
            background-color: $opacity-main-40;
        }
    }
</style>
