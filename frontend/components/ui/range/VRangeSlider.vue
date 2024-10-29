<script setup lang="ts">
// #region Imports
import useRangeSlider from '@idaproject/core/composables/ui/range/useRangeSlider';
import useRangeSliderProgress
    from '@idaproject/core/composables/ui/range/useRangeSliderProgress';
import useRangeSliderSize from '@idaproject/core/composables/ui/range/useRangeSliderSize';
import { splitThousands } from '@idaproject/core/assets/js/utils/numbers-utils';
import type { VRangeSliderProps } from './types';
import VRangeSliderDot from '~/components/ui/range/VRangeSliderDot.vue'; // #endregion
// #endregion

// #region Props
const {
    min = 0,
    max = 100,
    step = 1,
    modelValue = 0,
    range = false,
    vertical = false,
    height = '',
    disabled = false,
    showStops = false,
    showValue = false,
    valueFormat = splitThousands,
    marks = {},
    noTransition = false,
    theme = 'light',
    color = 'primary',
} = defineProps<VRangeSliderProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    dragstart: [],
    dragend: [],
    'update:modelValue': [value: number | number[]],
    change: [value: number | number[]],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const railRef = ref<HTMLElement | null>(null);
const dot1Ref = ref<InstanceType<typeof VRangeSliderDot> | null>(null);
const dot2Ref = ref<InstanceType<typeof VRangeSliderDot> | null>(null);

const { sliderSize } = useRangeSliderSize(railRef, vertical);

const {
    firstValue,
    secondValue,
    minValue,
    maxValue,
    precision,
    stops,
    markList,
    railStyle,
    formattedValue,
    dragging,
    focusDotIndex,
    onDragStart,
    onDragEnd,
    onRailClick,
    emitChange,
} = useRangeSlider(emit, toRef(() => min), toRef(() => max), toRef(() => step), showStops, vertical, toRef(() => range), toRef(() => marks), toRef(() => height), valueFormat, toRef(() => modelValue), sliderSize, dot1Ref, dot2Ref, railRef, toRef(() => disabled));

const { progressStyle } = useRangeSliderProgress(min, max, minValue, maxValue, firstValue, range, vertical, dragging, noTransition);
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${color}`]]: color,
        [$style._disabled]: disabled,
        [$style._vertical]: vertical,
        [$style._single]: !range,
    },
]);

// #endregion


// #endregion
</script>

<template>
    <div
        :class="[$style.VRangeSlider, classList]"
        role="slider"
        :aria-valuemin="min"
        :aria-valuemax="max"
        :aria-valuenow="range ? `${firstValue}-${secondValue}`: firstValue"
        :aria-orientation="vertical ? 'vertical': 'horizontal'"
        :aria-label="`slider between ${min} and ${max}`"
        :aria-disabled="disabled"
    >
        <div
            v-if="showValue"
            :class="$style.values"
        >
            <div
                :class="[$style.val, $style.subtitle]"
            >
                {{ range ? (formattedValue as number[])[0] : formattedValue }}
            </div>
            <div
                v-if="range"
                :class="[$style.val, $style.subtitle]"
            >
                {{ (formattedValue as number[])[1] }}
            </div>
        </div>

        <div
            ref="railRef"
            :class="$style.rail"
            :style="railStyle"
            @click="onRailClick"
        >
            <div :class="$style.track">
                <div
                    :class="$style.progress"
                    :style="progressStyle"
                >
                </div>

                <VRangeSliderDot
                    ref="dot1Ref"
                    v-model="firstValue"
                    :vertical="vertical"
                    :dragging="dragging || noTransition"
                    :focus="focusDotIndex === 0"
                    :slider-size="sliderSize"
                    :precision="precision"
                    :min="min"
                    :max="max"
                    :step="step"
                    :disabled="disabled"
                    @dragstart="onDragStart(0)"
                    @dragend="onDragEnd"
                    @emit-change="emitChange"
                />

                <VRangeSliderDot
                    v-if="range"
                    ref="dot2Ref"
                    v-model="secondValue"
                    :vertical="vertical"
                    :dragging="dragging || noTransition"
                    :focus="focusDotIndex === 1"
                    :slider-size="sliderSize"
                    :precision="precision"
                    :min="min"
                    :max="max"
                    :step="step"
                    :disabled="disabled"
                    @dragstart="onDragStart(1)"
                    @dragend="onDragEnd"
                    @emit-change="emitChange"
                />

                <template v-if="showStops && !markList.length">
                    <div
                        v-for="(stop, index) in stops"
                        :key="index"
                        :class="$style.stop"
                        :style="[vertical ? {bottom: stop + '%'} : {left: stop + '%'}]"
                    >
                    </div>
                </template>

                <template v-if="markList.length">
                    <div>
                        <div
                            v-for="item in markList"
                            :key="item.point"
                            :class="$style.stop"
                            :style="[vertical ? {bottom: item.position + '%'} : {left: item.position + '%'}]"
                        >
                        </div>
                    </div>

                    <div :class="$style.marks">
                        <div
                            v-for="item in markList"
                            :key="item.point"
                            :class="$style.marksText"
                            :style="[
                                vertical ? {bottom: item.position + '%'} : {left: item.position + '%'},
                                item.mark.style ? item.mark.style : '']"
                        >
                            {{ item.mark.label ? item.mark.label : item.mark }}
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<style lang="scss" module>
    $marks-color: $base-400;
    $progress-color: $primary-100;

    .VRangeSlider {

        /* Colors */
        &._light {
            &._primary {
                .rail:after {
                    background-color: rgba($primary-600, .3);
                }

                .track {
                    background-color: transparent;
                }
            }
        }

        /* Modificators */
        &._disabled {
            .track,
            .progress {
                background-color: $base-400;
            }

            .rail {
                cursor: default;
            }
        }

        .rail {
            position: relative;
            width: calc(100% - .8rem);
            height: 2rem;
            margin: 0 1rem;
            cursor: pointer;

            &:after {
                content: "";
                position: absolute;
                top: 50%;
                z-index: 1;
                width: 100%;
                height: 2px;
            }
        }

        .track {
            position: relative;
            top: 50%;
            z-index: 3;
            width: 100%;
            height: 2px;
            border-radius: 6px;
        }

        .progress {
            position: absolute;
            height: 100%;
            background-color: $primary-600;
        }

        .stop {
            position: absolute;
            width: 8px;
            height: 8px;
            border-radius: 100%;
            background-color: #fff;
            transform: translateX(-50%);
        }

        .marks {
            top: 0;
            left: 1.2rem;
            width: 1.8rem;
            height: 100%;
        }

        .marksText {
            position: absolute;
            margin-top: 1.5rem;
            font-size: 1.4rem;
            color: $marks-color;
            transform: translateX(-50%);
        }

        .values {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1.4rem;
        }

        .val {
            color: $base-0;
        }
    }
</style>
