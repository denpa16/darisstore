<script
    setup
    lang="ts"
>


/**
 * Позволяет пользователю ввести OTP код с помощью клавиатуры.<br>
 *
 * @version 1.1.0
 * @displayName VInputOtp
 */

// #region Imports
import type { InputOtpProps } from './types';
import { ColorsEnum, SizeEnum, ThemeEnum } from '@/types/ui/type.ts';
// #endregion

// #region Props
const {
    size = SizeEnum.medium,
    theme = ThemeEnum.light,
    color = ColorsEnum.primary,
    modelValue = '',
    label = '',
    placeholder = '0',
    msg = '',
    error,
    disabled,
    required,
    name,
} = defineProps<InputOtpProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    focus: [value: FocusEvent],
    blur: [value: FocusEvent],
    'update:modelValue': [value: string],
    'reset-error': [],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const inputsRefs = ref<{ [key: string]: object }>({});
const digits = ref<string[]>(['', '', '', '']);
const focusedIndex = ref<number>(-1);
const isFocused = ref<boolean>(false);
// #endregion

const labelString = computed(() => required ? label + '<span>*</span>' : label);

const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${color}`]]: color,
        [$style[`_${size}`]]: size,
        [$style._active]: modelValue || true,
        [$style._focused]: isFocused.value,
        [$style._disabled]: disabled,
        [$style._error]: error,
        [$style._showLabel]: Boolean(label),
    },
]);

const isFilled = computed((): boolean => digits.value.every(item => item !== ''));
// #endregion

// #region Methods
function addInputRef(el: object, id: number) {
    inputsRefs.value[id] = el;
}

function handleInput(index: number) {
    if (/^\d$/.test(digits.value[index])) {
        if (index < 3 && digits.value[index]) {
            inputsRefs.value[index + 1].focus();
        }
    } else {
        digits.value[index] = '';
    }

    if (isFilled.value) {
        emit('update:modelValue', digits.value.join(''));
    }
}

function handleKeyDown(event: KeyboardEvent, index: number) {
    if (event.key === 'Backspace' && !digits.value[index] && index > 0) {
        inputsRefs.value[index - 1].focus();
    }
}

function handlePaste(e) {
    e.preventDefault();
    const paste = (e.clipboardData || window.clipboardData).getData('text');
    if (/^\d{4}$/.test(paste)) {
        digits.value = paste.split('');

        for (let i = digits.value.length - 1; i >= 0; i--) {
            if (digits.value[i]) {
                inputsRefs.value[i].focus();
                break;
            }
        }

        if (isFilled.value) {
            emit('update:modelValue', digits.value.join(''));
        }

        handleBlur();
    }
}

function handleFocus(index: number) {
    focusedIndex.value = index;
    isFocused.value = true;
    emit('reset-error');
}

function handleBlur() {
    focusedIndex.value = -1;
    isFocused.value = false;
}

// #endregion
</script>

<template>
    <div :class="[$style.VInputOtp, classList]">
        <div :class="$style.inner">
            <input
                v-for="(_, index) in 4"
                :key="`code_${index}`"
                :ref="el => addInputRef(el, index)"
                v-model="digits[index]"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                :aria-label="label"
                :class="$style.native"
                :tabindex="index"
                :placeholder="placeholder"
                :name="name"
                :data-test-id="name"
                @blur="handleBlur"
                @focus="handleFocus(index)"
                @input="handleInput(index)"
                @keydown="handleKeyDown($event, index)"
                @paste.stop="handlePaste"
            >
        </div>

        <div
            v-if="label"
            :class="$style.label"
        >
            <div
                :class="$style.text"
                v-html="labelString"
            >
            </div>
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

<style
    lang="scss"
    module
>
    $grey-color: $base-200;
    $black-color: $base-900;
    $base-0-color: $base-0;

    .VInputOtp {
        position: relative;
        width: 100%;

        /* Sizes */
        &._medium {
            &._showLabel {
                padding-top: 2.8rem;
            }

            .inner {
                display: flex;
                align-items: center;
                height: 4.8rem;
                padding: 0 1.6rem;
            }

            .native {
                @include text(l1u);

                line-height: 1;

                &:not(:last-child) {
                    margin-right: .8rem;
                    padding-right: .8rem;
                    border-right: 1px solid $base-400;
                }

                @include respond-to(mobile) {
                    // Обязательно в px и не меньше 16px, чтобы не был автозума на айфонах
                    font-size: 16px;
                }
            }

            .label {
                @include text(l3);

                display: flex;
                align-items: center;

                .icon {
                    margin-left: .8rem;
                }
            }

            .icon {
                width: 1.6rem;
                height: 1.6rem;
                margin-left: .8rem;

                &._prefix {
                    margin-left: 0;
                }
            }
        }

        /* Colors */
        &._light {
            &._primary {
                &:not(._error, ._disabled,._success) {
                    @include hover {
                        &:hover {
                            .inner {
                                border-color: $base-400;
                            }

                            &._arrowUp {
                                .inner {
                                    border-color: $black-color;
                                }
                            }

                            &:not(._hasArrow) {
                                &._focused {
                                    .inner {
                                        border-color: $base-400;
                                    }
                                }
                            }
                        }
                    }

                    &._arrowUp {
                        .inner {
                            border-color: $black-color;
                        }
                    }

                    &:not(._hasArrow) {
                        &._focused {
                            .inner {
                                border-color: $base-400;
                            }
                        }
                    }
                }

                .inner {
                    border: 1px solid $grey-color;
                    transition: border $default-transition;
                }

                input.native {
                    color: $black-color;

                    &:not(:last-child) {
                        border-color: $base-400;
                    }
                }

                .label {
                    color: $black-color;

                    span {
                        color: $primary-900;
                    }
                }

                .icon {
                    color: $grey-color;
                }

                ::placeholder {
                    color: $base-500;
                }

                &._disabled {
                    .icon {
                        color: $base-100;
                    }

                    ::placeholder,
                    input.native {
                        color: $base-200;
                    }
                }
            }
        }

        /* Mods */
        &._showLabel {
            .label {
                opacity: 1;
                transition: .3s all ease;
            }
        }

        &._active {
            .inner:after {
                transform: scaleX(1);
            }
        }

        &._error {
            &._light {
                .inner {
                    border-color: $primary-900;
                }
            }
        }

        &._disabled {
            cursor: not-allowed;

            .inner,
            .icon {
                pointer-events: none;
            }

            ::placeholder {
                user-select: none;
            }
        }
    }

    .native,
    .label {
        font-weight: normal;
    }

    .native {
        width: 100%;
        text-align: center;
    }

    .label {
        position: absolute;
        top: 0;
        transition: opacity $default-transition;
        pointer-events: none;
    }

    .inner {
        position: relative;
        z-index: 2;

        .icon {
            &._calendar {
                width: 2rem;
                height: 2rem;
                color: $base-200;
            }
        }
    }

    .icon {
        flex-shrink: 0;
        pointer-events: all;
        transition: $default-transition;

        &._up {
            transform: rotate(180deg);
        }

        &._calendar {
            width: 2rem;
            height: 2rem;
            color: $base-200;
        }
    }
</style>
