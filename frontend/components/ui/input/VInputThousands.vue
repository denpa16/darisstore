<script setup lang="ts">
// #region Imports
import { setCursor } from '@idaproject/core/assets/js/utils/mask-utils';
import type { InputThousandsProps } from './types.ts';
// #endregion

// #region Props
const {
    size = 'medium',
    theme = 'light',
    color = 'primary',
    modelValue = '',
    disabled,
    delimiter = ' ',
    decimalMark = '.',
    decimalCount = 2,
    positiveOnly = false,
    length = { maxlength: 524288, minlength: 0 },
    name = '',
} = defineProps<InputThousandsProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    change: [value: string],
    focus: [value: FocusEvent],
    blur: [value: FocusEvent],
    'update:modelValue': [value: string],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const isFocused = ref(false);
const splittedValue = ref(stripValue(modelValue));
const attrs = useAttrs();
// #endregion

// #region Computed
const attributes = computed(() => {
    let attrsValue = {
        ...attrs,
        disabled,
        maxlength: 524288,
        minlength: 0,
    };


    if (Object.values(length).length) {
        attrsValue = {
            ...attrsValue,
            ...length,
        };
    }

    return attrsValue;
});

const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${color}`]]: color,
        [$style[`_${size}`]]: size,
        [$style._focused]: isFocused.value,
        [$style._disabled]: disabled,
    },
]);

const cleanValue = computed(() => splittedValue.value.split(delimiter)
    .join(''));

// #endregion

// #region Watch
watch(() => modelValue, val => {
    if (val !== cleanValue.value) {
        splittedValue.value = stripValue(val);
    }
});
// #endregion

// #region Methods
function onChange() {
    if (splittedValue.value.length > 1 && splittedValue.value[0] === '0') {
        splittedValue.value = stripValue(cleanValue.value.toString()
            .replace(/^(-)?0+(?=\d)/, '$1'));
    }

    if (!splittedValue.value || splittedValue.value === '0') {
        splittedValue.value = '';
    }

    nextTick(() => {
        emit('change', cleanValue.value);
    });
}

function onFocus(e: FocusEvent) {
    isFocused.value = true;
    emit('focus', e);
}

function onBlur(e: FocusEvent) {
    isFocused.value = false;
    onChange();
    emit('blur', e);
}

function onInput(e: Event) {
    let endPos = (e.target as HTMLInputElement).selectionEnd || 0;
    const target = (e.target as HTMLInputElement);
    const oldValue = target.value;
    const newValue = stripValue(target.value);
    target.value = newValue;
    splittedValue.value = newValue;

    nextTick(() => {
        endPos = getNextCursorPosition(endPos, oldValue, newValue, delimiter);
        setCursor(target, endPos);
        emit('update:modelValue', cleanValue.value);
    });
}

function onEnter(e: KeyboardEvent) {
    (e.target as HTMLInputElement).blur();
}

function stripValue(value: string) {
    if (!value) {
        return '';
    }

    let partDecimal = '';
    let parts;

    // strip alphabet letters
    value = value.toString();
    value = value
        .replace(/[A-Za-z]/g, '')
        // replace the first decimal mark with reserved placeholder
        .replace(decimalMark, 'M')

        // strip non numeric letters except minus and "M"
        // this is to ensure prefix has been stripped
        .replace(/[^\dM-]/g, '')

        // replace the leading minus with reserved placeholder
        .replace(/^-/, 'N')

        // strip the other minus sign (if present)
        .replace(/-/g, '')

        // replace the minus sign (if present)
        .replace('N', positiveOnly ? '' : '-')

        // replace decimal mark
        .replace('M', decimalMark);

    const partSign = value.slice(0, 1) === '-' ? '-' : '';
    const partSignAndPrefix = partSign;
    let partInteger = value;

    if (value.includes(decimalMark)) {
        parts = value.split(decimalMark);
        partInteger = parts[0];
        partDecimal = `${decimalMark}${parts[1].slice(0, decimalCount)}`;
    }

    if (partSign === '-') {
        partInteger = partInteger.slice(1);
    }

    partInteger = partInteger.replace(/(\d)(?=(\d{3})+$)/g, '$1' + delimiter);

    return (
        partSignAndPrefix +
        partInteger +
        (decimalCount > 0 ? partDecimal : '')
    );
}

function getNextCursorPosition(prevPos: number, oldValue: string, newValue: string, delimiter: string) {
    return oldValue.length === prevPos
        ? newValue.length
        : prevPos + getPositionOffset(prevPos, oldValue, newValue, delimiter);
}

function getPositionOffset(prevPos: number, oldValue: string, newValue: string, delimiter: string) {
    const oldRawValue = stripDelimiters(oldValue.slice(0, prevPos), delimiter);
    const newRawValue = stripDelimiters(newValue.slice(0, prevPos), delimiter);
    const lengthOffset = oldRawValue.length - newRawValue.length;
    return lengthOffset !== 0 ? lengthOffset / Math.abs(lengthOffset) : 0;
}

function stripDelimiters(value: string, delimiter: string) {
    const delimiterRE = delimiter
        ? new RegExp(delimiter.replace(/([.?*+^$[\]\\(){}|-])/g, '\\$1'), 'g')
        : '';
    return value.replace(delimiterRE, '');
}

// #endregion
</script>

<template>
    <div :class="['v-input', $style.VInputThousands, classList]">
        <div :class="['v-input__inner', $style.inner]">
            <input
                ref="input"
                :class="[$style.native]"
                v-bind="attributes"
                :value="splittedValue"
                type="text"
                inputmode="numeric"
                :name="name"
                :data-test-id="name"
                @keydown.enter="onEnter"
                @input="onInput"
                @change="onChange"
                @focus="onFocus"
                @blur="onBlur"
            >
        </div>
    </div>
</template>

<style lang="scss" module>
    $base-0-color: $base-0;
    $black-color: $base-600;

    .VInputThousands {
        position: relative;
        width: 100%;

        /* Sizes */
        &._medium {
            input.native {
                width: 100%;
                font-size: 1.4rem;
                font-weight: 500;
                line-height: 1;

                @include respond-to(mobile) {
                    // Обязательно в px и не меньше 16px, чтобы не был автозума на айфонах
                    font-size: 16px;
                }
            }
        }

        /* Themes */
        &._light {
            &._primary {
                input.native {
                    color: $black-color;
                }
            }
        }

        &._dark {
            &._primary {
                input.native {
                    color: $base-0-color;
                }
            }
        }

        /* Modificators */
        &._focused {
            //
        }

        &._disabled {
            pointer-events: none;

            input.native {
                -webkit-text-fill-color: $base-400;
                color: $base-400;
            }

            select.nativeSelect {
                pointer-events: none;
            }
        }
    }

    input.native {
        transition: color $default-transition;
    }

    .inner {
        position: relative;
        z-index: 2;
    }
</style>
