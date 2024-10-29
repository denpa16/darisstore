<script setup
        lang="ts"
>
/**
 * Позволяет пользователю ввести данные в рамках диапазона, например цены или площади.<br>
 * Включает в себя два компонента, VSilder и VInputThousands (для разбиение цены на тысячные).
 *
 * У нас на проектах применяется принцип "фасетного фильтра", т.е.:<br><br>
 *
 * <strong>specs</strong> - диапазон всех доступных значений.<br>
 * <strong>facets</strong> - значения, которые доступны после передачи параметров из
 * <strong>value</strong>.<br><br>
 *
 * <a href="https://habr.com/ru/post/517074/" target="_blank">
 *     Подробнее про работу фасетных фильтров
 * </a>
 * @version 1.0.4
 * @displayName VRange
 */

// #region Imports
import useRange from '@idaproject/core/composables/ui/range/useRange';
import useRangePlaceholder from '@idaproject/core/composables/ui/range/useRangePlaceholder';
import useRangeSizes from '@idaproject/core/composables/ui/range/useRangeSizes';
import type { VRangeProps } from './types';
import type { ChoiceLabel, RangeValue } from '~/types/filter'; // #endregion
// #endregion

// #region Props
const {
    name,
    size = 'medium',
    theme = 'light',
    color = 'primary',
    label = '',
    postfix = '',
    prefixes = [],
    bottomLabels = [],
    specs,
    facets = { min: 0, max: Infinity },
    step = 1,
    valueMin = 0,
    valueMax = Infinity,
    single,
    disabled,
    positiveOnly = true,
    showPercent,
    valueFilter,
    valueParser,
    dynamicInputWidth,
    decimalCount = 0,
    decimalMark = '.',
} = defineProps<VRangeProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    change: [value: RangeValue | number | Record<ChoiceLabel, RangeValue | number>],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const isFirstInputFocused = ref<boolean>(false);
const isSecondInputFocused = ref<boolean>(false);

const placeholderRef = ref<HTMLElement | null>(null);
const minPlaceholderRef = ref<HTMLElement | null>(null);
const maxPlaceholderRef = ref<HTMLElement | null>(null);


const {
    percent,
    firstInputValue,
    secondInputValue,
    inputsLength,
    sliderModel,
    isLazyChange,
    onInputChange,
    emitChange,
    onSliderUpdate,
} = useRange(emit, name, toRef(() => valueMin), toRef(() => valueMax), toRef(() => facets), toRef(() => specs), decimalCount, single, valueParser, valueFilter);

const {
    placeholderFirstValue,
    placeholderSecondValue,
    onInput,
} = useRangePlaceholder(isLazyChange, firstInputValue, secondInputValue, decimalMark, single);

const {
    inputsStyle,
    getStylesMin,
    getStylesMax,
} = useRangeSizes(dynamicInputWidth, minPlaceholderRef, maxPlaceholderRef, placeholderRef, single);
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${color}`]]: color,
        [$style[`_${size}`]]: size,
        [$style._disabled]: disabled,
        [$style._isFirstInputFocused]: isFirstInputFocused.value,
        [$style._isSecondInputFocused]: isSecondInputFocused.value,
    },
]);

const minName = computed(() => {
    if (name) {
        return single ? name : name + 'Min';
    }

    return '';
});
// #endregion
</script>

<template>
    <div :class="[$style.VRange, classList]">
        <div
            v-if="label"
            :class="$style.label"
            v-html="label"
        />
        <div
            :style="inputsStyle"
            :class="$style.inputs"
        >
            <div :class="$style.divider"></div>
            <div :class="$style.inputWrapper">
                <div :class="[$style.inputArea, $style._first]">
                    <div
                        v-if="prefixes[0]"
                        :class="$style.prefix"
                    >
                        {{ prefixes[0] }}
                    </div>

                    <VInputThousands
                        :color="color"
                        :size="size"
                        :model-value="firstInputValue"
                        :style="getStylesMin"
                        :class="$style.input"
                        :positive-only="positiveOnly"
                        :length="inputsLength"
                        :decimal-count="decimalCount"
                        :disabled="disabled"
                        :name="minName"
                        @update:model-value="onInput($event, 'first')"
                        @change="onInputChange($event, 'first')"
                        @focus="isFirstInputFocused = true"
                        @blur="isFirstInputFocused = false"
                    />

                    <div
                        v-if="postfix"
                        :class="$style.postfix"
                        v-html="postfix"
                    >
                    </div>
                </div>
            </div>

            <div
                v-if="showPercent"
                :class="$style.percent"
            >
                {{ percent }}%
            </div>

            <div
                v-if="!single"
                :class="[$style.inputWrapper, $style._second]"
            >
                <div :class="[$style.inputArea, $style._second]">
                    <div
                        v-if="prefixes[1]"
                        :class="$style.prefix"
                    >
                        {{ prefixes[1] }}
                    </div>

                    <VInputThousands
                        :model-value="secondInputValue"
                        :color="color"
                        :size="size"
                        :style="getStylesMax"
                        :class="$style.input"
                        :positive-only="positiveOnly"
                        :length="inputsLength"
                        :disabled="disabled"
                        :name="name ? name + 'Max' : ''"
                        @update:model-value="onInput($event, 'second')"
                        @change="onInputChange($event, 'second')"
                        @focus="isSecondInputFocused = true"
                        @blur="isSecondInputFocused = false"
                    />

                    <div
                        v-if="postfix"
                        :class="$style.postfix"
                        v-html="postfix"
                    >
                    </div>
                </div>
            </div>
        </div>

        <VRangeSlider
            :model-value="sliderModel"
            :theme="theme"
            :color="color"
            :min="specs.min"
            :max="specs.max"
            :step="step"
            :range="!single"
            :class="$style.slider"
            :disabled="disabled"
            @change="emitChange"
            @update:model-value="onSliderUpdate"
        />

        <div
            v-if="bottomLabels.length"
            :class="$style.bottomLabels"
        >
            <div
                v-if="bottomLabels[0]"
                :class="$style.bottomLabel"
            >
                {{ bottomLabels[0] }}
            </div>
            <div
                v-if="bottomLabels[1]"
                :class="$style.bottomLabel"
            >
                {{ bottomLabels[1] }}
            </div>
        </div>

        <div
            v-if="dynamicInputWidth"
            ref="placeholderRef"
            :class="$style.placeholder"
        >
            <span
                ref="minPlaceholderRef"
                v-html="placeholderFirstValue"
            >
            </span>

            <span
                v-if="!single"
                ref="maxPlaceholderRef"
                v-html="placeholderSecondValue"
            >
            </span>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    .VRange {
        display: flex;
        flex-direction: column;
        font-size: 1.4rem;
        font-weight: 500;

        @include respond-to(mobile) {
            // Обязательно в px и не меньше 16px, чтобы не был автозума на айфонах
            font-size: 16px;
        }

        /* Sizes */
        &._medium {
            height: 4rem;

            .inputArea {
                padding: .8rem 1.2rem 1rem 1.8rem;
                border-radius: .8rem;
                border: 1px solid transparent;

                &._second {
                    padding-right: 1.8rem;
                    padding-left: 1.2rem;

                    input {
                        text-align: right;
                    }
                }
            }

            .prefix {
                margin-right: .4rem;
            }

            .postfix {
                margin-left: .4rem;
            }

            .native {
                width: 100%;
            }
        }

        /* Colors */
        &._light {
            &._primary {
                .inputs {
                    border: 1px solid $base-200;
                    background-color: $base-0;
                }

                .prefix {
                    color: $base-600;
                }
            }
        }

        /* Modificators */
        &._disabled {
            pointer-events: none;

            select.nativeSelect {
                pointer-events: none;
            }

            .label,
            .input,
            .percent,
            .prefix,
            .postfix {
                color: $base-400;
            }
        }
    }

    .label {
        margin-bottom: .8rem;
        font-size: 1.2rem;
        font-weight: 500;
        line-height: 112%;
    }

    .inputs {
        position: relative;
        visibility: hidden;
        display: flex;
        justify-content: space-between;
        border-radius: .8rem;
        border: 1px solid transparent;
        line-height: 1;
        opacity: 0;
        transition: $default-transition;

        input {
            @include respond-to(tablet) {
                width: 100%;
            }
        }
    }

    .inputWrapper {
        position: relative;
        display: inline-flex;
        align-items: center;
        flex-grow: 1;
        width: 50%;
        height: 100%;

        &._second {
            justify-content: right;
        }
    }

    .inputArea {
        display: flex;
        align-items: center;
        font-weight: 500;
        transition: $default-transition;
    }

    .divider {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 1px;
        height: 1.2rem;
        background-color: $base-400;
        opacity: .3;
        transform: translateY(-50%);
    }

    .percent {
        position: absolute;
        top: 50%;
        right: 2rem;
        font-size: inherit;
        color: $base-400;
        transform: translateY(-50%);
    }

    .postfix,
    .prefix {
        cursor: default;
        user-select: none;
    }

    .slider {
        width: calc(100% - 2.4rem);
        margin-top: -1.2rem;
        margin-left: .6rem;
    }

    .bottomLabels {
        @include text(l6-book);

        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-top: 2rem;
        color: $base-400;
    }

    .placeholder {
        position: absolute;
        z-index: -1;
        visibility: hidden;
        font-size: inherit;
        font-weight: bold;
        letter-spacing: initial;
        cursor: default;
    }
</style>
