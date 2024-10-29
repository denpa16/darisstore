<script setup lang="ts">


/**
     * Позволяет пользователю ввести данные с помощью клавиатуры.<br>
     * Можно использовать вместе с утилитами из validate-utils, для проверки корректности ввода, по заданному параметру.
     *
     * @version 1.1.0
     * @displayName VInput
 */

// #region Imports
import useInput from '@idaproject/core/composables/ui/useInput';
import type { InputProps } from './types';
import InputSearchResults from '~/components/ui/input/InputSearchResults.vue';
import { ColorsEnum, SizeEnum, ThemeEnum } from '@/types/ui/type.ts';
// #endregion

// #region Props
const {
    size = SizeEnum.medium,
    sizeClearBtn = SizeEnum.medium,
    color = ColorsEnum.primary,
    theme = ThemeEnum.light,
    type = 'text',
    modelValue = '',
    autocomplete = true,
    autocompleteName = '',
    label = '',
    placeholder = '',
    msg = '',
    prefixIcon = '',
    suffixIcon = '',
    suffixColor = '',
    mask = '',
    premask = true,
    keepMasked = true,
    error,
    disabled,
    info,
    infoRight,
    readonly,
    arrowState = null,
    pointer,
    required,
    name,
    isSearch = false,
    absoluteHint = false,
    isClearBtn = false,
    results = null,
    fullWidth = false,
    calendar = false,
    lettersOnly = false,
} = defineProps<InputProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    focus: [value: FocusEvent],
    blur: [value: FocusEvent],
    input: [value: Event],
    'input-click': [value: MouseEvent],
    'update:modelValue': [value: string],
    'search-update': [value: object],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const attrs = useAttrs();

const {
    isFocused,
    currentMask,
    inputValue,
    currentPremask,
    attributes,
    onFocus,
    onBlur,
    onInput,
    onKeyDown,
    onPaste,
    clear,
} = useInput(emit, toRef(() => mask), toRef(() => modelValue), label, autocomplete, autocompleteName, type, readonly, attrs, lettersOnly, keepMasked);
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
        [$style._hasPrefixIcon]: prefixIcon,
        [$style._pointer]: pointer,
        [$style._arrowUp]: arrowState,
        [$style._search]: isSearch,
        [$style._hasArrow]: arrowState !== null,
        [$style._hideMask]: !modelValue && placeholder,
        [$style._success]: mask && !error && currentMask.value.length === inputValue.value.length,
        [$style._clearBtn]: isClearBtn,
        [$style._fillWidth]: fullWidth,
    },
]);
    // #endregion

// #region Methods

// #endregion
</script>

<template>
    <div :class="[$style.VInput, classList]">
        <div
            :class="$style.inner"
            @click="emit('input-click', $event)"
        >
            <VIcon
                v-if="prefixIcon"
                :class="[$style.icon, $style._prefix]"
                :name="prefixIcon"
            />

            <input
                v-bind="attributes"
                :aria-label="label"
                :class="$style.native"
                :tabindex="0"
                :value="inputValue"
                :placeholder="placeholder"
                :name="name"
                :data-test-id="name"
                @blur="onBlur"
                @focus="onFocus"
                @input="onInput"
                @keydown="onKeyDown"
                @paste.stop="onPaste"
            >

            <VIcon
                v-if="suffixIcon"
                :class="[$style.icon, $style.suffix, {
                    [$style[`_${suffixColor}`]]: suffixColor,
                    [$style._calendar]: calendar,
                }]"
                :name="suffixIcon"
            />

            <VTooltip
                v-if="infoRight"
                :class="$style.icon"
                :text="infoRight"
            >
                <template #activator>
                    <VIcon name="information" />
                </template>
            </VTooltip>

            <VIcon
                v-if="arrowState !== null"
                :class="[$style.icon, $style._arrow, {[$style._up]: arrowState}]"
                name="arrow-down"
            />

            <div
                v-if="premask"
                :class="$style.premask"
                v-html="currentPremask"
            >
            </div>
        </div>

        <VButton
            v-if="inputValue && isClearBtn"
            :class="$style.clearBtn"
            :size="sizeClearBtn"
            border
            round
            equal
            @click="clear"
        >
            <VIcon
                size="medium"
                name="close"
            />
        </VButton>

        <div
            v-if="label"
            :class="$style.label"
        >
            <div
                :class="$style.text"
                v-html="labelString"
            >
            </div>

            <VTooltip
                v-if="info"
                :class="$style.icon"
                :text="info"
            >
                <template #activator>
                    <VIcon name="information" />
                </template>
            </VTooltip>
        </div>

        <transition name="dropdown">
            <div
                v-if="isSearch && results && results.length"
                :class="$style.dropdown"
                @mousedown.stop.prevent
            >
                <VScrollBox
                    :class="$style.scrollbox"
                    resizable
                >
                    <InputSearchResults
                        :results="results"
                        @click="emit('search-update', $event)"
                    />
                </VScrollBox>
            </div>
        </transition>

        <transition name="fade-fast">
            <InputHint
                v-if="msg"
                :absolute="isSearch || absoluteHint"
                :theme="error ? 'alert' : theme"
                :disabled="disabled"
            >
                {{ msg }}
            </InputHint>
        </transition>
    </div>
</template>

<style lang="scss" module>
    $grey-color: $base-200;
    $black-color: $base-900;
    $base-0-color: $base-0;

    .VInput {
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

            .premask {
                margin-left: 2rem;
            }

            .premask,
            .native {
                @include text(l1u);

                height: 100%;
                line-height: 1;

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

                ::placeholder,
                .premask {
                    color: $base-500;
                }

                &._active {
                    .premask {
                        opacity: 1;
                    }
                }

                &._disabled {
                    .icon {
                        color: $base-100;
                    }

                    ::placeholder,
                    .premask,
                    input.native {
                        color: $base-200;
                    }
                }

                .dropdown {
                    background: $base-0-color;
                    color: $black-color;
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

            .premask {
                opacity: .5;

                span {
                    opacity: 0;
                }
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

        &._hasPrefixIcon {
            .inner {
                padding-left: 2rem;
            }

            .native {
                margin-left: 1.2rem;
            }

            .premask {
                width: calc(100% - 4.8rem);
                margin-left: 4.8rem;
            }
        }

        &._pointer {
            .inner {
                cursor: pointer;
            }

            input {
                cursor: pointer;
            }
        }

        &._hideMask {
            .premask {
                display: none;
            }
        }

        &._clearBtn {
            display: flex;
            align-items: center;
        }

        &._fillWidth {
            width: 100%;

            .inner {
                width: 100%;
            }
        }

        .suffix {
            // colors
            &._dark {
                color: $base-200;
            }
        }
    }

    .premask,
    .native,
    .label {
        font-weight: normal;
    }

    .premask,
    .native {
        width: 100%;
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

    .premask {
        position: absolute;
        top: 50%;
        left: 0;
        z-index: 1;
        display: inline-flex;
        align-items: center;
        margin: 0;
        opacity: 0;
        transform: translateY(-50%);
        transition: opacity $default-transition;
        user-select: none;
        pointer-events: none;

        @include respond-to(mobile) {
            bottom: -.3rem;
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

    .dropdown {
        position: absolute;
        top: calc(100% + 1.2rem);
        left: 0;
        z-index: 10;
        display: block;
        width: 100%;
        padding: .8rem 0;
        border-radius: 1.2rem;
        transform: translate3d(0, 0, 0);
        transition: opacity .2s ease, transform .2s ease;
        box-shadow: 8px 8px 30px rgb(0 0 0 / 12%);

        .scrollbox {
            max-height: 18rem;
        }
    }

    .clearBtn {
        flex-shrink: 0;
        margin-left: .8rem;
    }
</style>
