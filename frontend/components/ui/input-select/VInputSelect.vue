<script setup
        lang="ts"
>
/**
 * Как и <a href="#VInput" style="color: #2963eb">VInput</a> служит для ввода данных,<br>
 * но также предоставляет возможность выбрать предустановленные данные из селекта<br>
 * Использует VInput, VSelectOption и VScrollbox<br><br>
 * Пример использования - любой список с ограниченным набором выходных данных, к примеру адреса
 *
 * @version 1.0.1
 * @displayName VInputSelect
 */

// #region Imports
// Vue
import { onClickOutside } from '@vueuse/core';

// Types
import type { Props } from './types.ts';
import { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils';
import type { Choice, ChoiceValue } from '~/types/filter';
// #endregion


// #region Props
const {
    size = 'medium',
    theme = 'light',
    color = 'primary',
    label = '',
    modelValue = '',
    keepLabel = true,
    msg = '',
    border = true,
    error = false,
    autocomplete = true,
    disabled = false,
    specs = [],
} = defineProps<Props>();
// #endregion

// #region Emits
const emit = defineEmits<{
    focus: [value: FocusEvent],
    blur: [value: FocusEvent],
    'update:modelValue': [value: ChoiceValue],
}>();
// #endregion

// #region Data
const isFocused = ref(false);
const highlightIndex = ref(-1);
const inputRef = ref<HTMLElement | null>(null);
const VInputSelectRef = ref<HTMLElement | null>(null);
// #endregion

// #region Computed
const classList = computed(() => ({
    [`_${theme}`]: theme,
    [`_${color}`]: color,
    [`_${size}`]: size,
    _active: modelValue || isFocused,
    _disabled: disabled,
}));

/**
 * пропы, которые будут прокинуты в VInput
 */
const inputProps = computed(() => ({
    size,
    color,
    label,
    modelValue,
    keepLabel,
    msg,
    border,
    error,
    autocomplete,
    disabled,
}));
// #endregion


// #region Lifecycle
onClickOutside(VInputSelectRef, () => clickOutside());
// #endregion

// #region Methods
function onSelectDropdownOption(e: Choice) {
    highlightIndex.value = -1;
    isFocused.value = false;
    emit('update:modelValue', e?.[choiceValueKey] ?? '');
}

async function clickOutside() {
    if (!isFocused.value) {
        return;
    }

    isFocused.value = false;
}

function onFocus(e: FocusEvent) {
    isFocused.value = true;
    emit('focus', e);
}

function onBlur(e: FocusEvent) {
    emit('blur', e);
}

function onInput(value: string) {
    emit('update:modelValue', value);
}

// #endregion
</script>

<template>
    <div
        ref="VInputSelectRef"
        :class="[$style.VInputSelect, classList]"
    >
        <VInput
            v-bind="inputProps"
            ref="inputRef"
            :class="$style.input"
            type="text"
            @focus="onFocus"
            @blur="onBlur"
            @update:model-value="onInput"
        />
        <transition name="dropdown">
            <div
                v-if="isFocused && specs.length"
                :class="$style.dropdown"
                @mousedown.stop.prevent
            >
                <VScrollBox
                    :class="$style.scrollbox"
                    resizable
                >
                    <VSelectOption
                        v-for="(option, index) in specs"
                        :key="`${option[choiceLabelKey]}-${index}`"
                        :option="option"
                        :value="modelValue"
                        :size="size"
                        :color="color"
                        :is-highlighted="highlightIndex === index"
                        @mouseenter="highlightIndex = index"
                        @mouseleave="highlightIndex = -1 "
                        @click="onSelectDropdownOption"
                    />
                </VScrollBox>
            </div>
        </transition>
    </div>
</template>

<style lang="scss"
       module
>
    $base-0-color: $base-0;
    $grey-color: $base-400;
    $black-color: $base-600;
    $active-color: $primary-100;

    .VInputSelect {
        position: relative;
        width: 100%;


        /* Themes */
        &._light {
            &._primary {
                .dropdown {
                    background: $base-0-color;
                    color: $black-color;
                }

                &:after {
                    background-color: $grey-color;
                }
            }
        }

        &._dark {
            &._primary {
                .dropdown {
                    background: $black-color;
                    color: $base-0-color;
                }

                &:after {
                    background-color: $grey-color;
                }
            }
        }
    }

    .dropdown {
        position: absolute;
        top: calc(100% + .2rem);
        left: 0;
        z-index: 10;
        display: block;
        width: 100%;
        padding: 1.2rem 0;
        border-radius: 1.2rem;
        transform: translate3d(0, 0, 0);
        transition: opacity .2s ease, transform .2s ease;
        box-shadow: 8px 8px 30px rgb(0 0 0 / 12%);

        .scrollbox {
            max-height: 18rem;
        }

        @include respond-to(tablet) {
            z-index: -1;
            display: none;
            pointer-events: auto;
        }
    }
</style>
