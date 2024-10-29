<script setup
        lang="ts"
>
// #region Imports
import useRangeSliderDot from '@idaproject/core/composables/ui/range/useRangeSliderDot';
import type { VRangeSliderDotProps } from './types'; // #endregion
// #endregion

// #region Props
const propsSource = withDefaults(defineProps<VRangeSliderDotProps>(), { modelValue: 0 });
const props = toRefs(propsSource);
// #endregion

// #region Emits
const emit = defineEmits<{
    dragstart: [],
    dragend: [],
    'update:modelValue': [value: number],
    'emit-change': [],
}>();
// #endregion

// #region Data
const $style = useCssModule();

const {
    styles,
    hovering,
    onMouseEnter,
    onMouseLeave,
    onLeftKeyDown,
    onRightKeyDown,
    onMouseDown,
    setPosition,
} = useRangeSliderDot(emit, props.modelValue, props.min, props.max, props.vertical, props.dragging, props.step, props.sliderSize, props.precision, props.disabled);
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._hover]: hovering.value,
        [$style._dragging]: props.dragging.value,
        [$style._disabled]: props.disabled.value,
    },
]);
// #endregion

// #region Lifecycle
defineExpose({
    setPosition,
});
// #endregion
</script>

<template>
    <div
        :class="[$style.VRangeSliderDot, classList]"
        :style="styles"
        tabindex="0"
        @focus="onMouseEnter"
        @blur="onMouseLeave"
        @mouseenter="onMouseEnter"
        @mouseleave="onMouseLeave"
        @mousedown.prevent="onMouseDown"
        @touchstart.prevent="onMouseDown"
        @keydown.left="onLeftKeyDown"
        @keydown.right="onRightKeyDown"
        @keydown.down.prevent="onLeftKeyDown"
        @keydown.up.prevent="onRightKeyDown"
    >

        <div :class="[$style.handle]"></div>
    </div>
</template>

<style lang="scss"
       module
>
    .VRangeSliderDot {
        position: absolute;
        top: 50%;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 1.6rem;
        height: 1.6rem;
        text-align: center;
        line-height: normal;
        transform: translate(-50%, -50%);
        user-select: none;

        .handle {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: $base-0;
            box-shadow: 0 .5px 4px 0 rgb(0 0 0 / 12%), 0 6px 13px 0 rgb(0 0 0 / 12%);
            user-select: none;

            @include hover {
                &:hover {
                    &:after {
                        width: calc(100% - .5rem);
                        height: calc(100% - .5rem);
                    }
                }
            }
        }

        &._disabled {
            .handle {
                background-color: $base-400;
            }
        }
    }
</style>
