<script setup
        lang="ts"
>
// #region Imports
// Types
import useSelectOption from '@idaproject/core/composables/ui/useSelectOption';
import type { OptionType, VSelectOptionProps } from './types.ts';
import { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils'; // Components
import type { ChoiceValue } from '~/types/filter'; // Pinia
import { useDeviceStore } from '@idaproject/core/store/device';
import { SizeEnum, ThemeEnum } from '@/types/ui/type.ts'; // Utils
// Components
const VCheckbox = defineAsyncComponent(() => import('~/components/ui/checkbox/VCheckbox.vue'));
// #endregion

// #region Props
const {
    option,
    value,
    valueName = choiceValueKey,
    labelName = choiceLabelKey,
    size = SizeEnum.medium,
    isHighlighted,
    multiple = false,
    theme = ThemeEnum.light,
    hasInner,
    innerValue = null,
    innerMultiple = false,
    innerResetLabel,
    nextSelected = false,
} = defineProps<VSelectOptionProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    click: [value: OptionType, innerOption: ChoiceValue | ChoiceValue[]],
    'set-inner': [option: OptionType, values: ChoiceValue | ChoiceValue[]],
    mouseenter: [],
    mouseleave: [],
}>();
// #endregion

// #region Data
const deviceStore = useDeviceStore();
const $style = useCssModule();

const { isSelected, innerValueFiltered, onInnerClick, initLazyInnerValue, onOptionClick } =
    useSelectOption(emit, multiple, toRef(() => value), option, valueName, innerMultiple, toRef(() => innerValue), hasInner);
// #endregion

const classList = computed(() => [
    {
        [$style[`_${size}`]]: size,
        [$style[`_${theme}`]]: theme,
        [$style._highlighted]: isHighlighted,
        [$style._selected]: isSelected.value,
        [$style._disabled]: option.disabled,
        [$style._multiple]: multiple,
        [$style._nextSelected]: nextSelected,
    },
]);
// #endregion


// #region Lifecycle
initLazyInnerValue();
// #endregion

// #region Methods
const onMouseEnter = () => {
    if (deviceStore.isTouch) {
        return;
    }

    emit('mouseenter');
};

const onMouseLeave = () => {
    if (deviceStore.isTouch) {
        return;
    }

    emit('mouseleave');
};
// #endregion
</script>

<template>
    <div
        :class="[$style.VSelectOption, classList]"
        @mouseenter="onMouseEnter"
        @mouseleave="onMouseLeave"
        @click="onOptionClick"
    >
        <div :class="$style.itemWrapper">
            <div
                :class="$style.itemHead"
            >
                <VCheckbox
                    v-if="multiple"
                    :model-value="isSelected"
                    :class="$style.checkbox"
                    @click.prevent
                />

                <slot>
                    {{ option[labelName] }}
                </slot>
            </div>

            <div
                v-if="hasInner && option.inner_specs && option.inner_specs.length > 1 && isSelected"
                :class="$style.itemBottom"
                @click.stop
            >
                <VTabBar
                    :specs="option.inner_specs"
                    :facets="option.inner_facets"
                    :model-value="innerValueFiltered"
                    size="small"
                    close
                    :multiple="innerMultiple"
                    flex-wrap
                    :reset-label="innerResetLabel"
                    @update:model-value="onInnerClick(($event as ChoiceValue | ChoiceValue[]))"
                />
            </div>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    .VSelectOption {
        white-space: nowrap;
        transition: $default-transition;
        cursor: pointer;

        /* Colors */
        &._light {
            color: $base-900;

            @include hover {
                background: $base-50;
            }
        }

        /* Sizes */
        &._medium {
            @include text(l2m);

            padding: 1.6rem 1.2rem;
        }

        /* Modificators */
        &:not(._multiple) {
            &._selected {
                background-color: $base-100;
            }
        }

        &._disabled {
            &:not(._selected) {
                opacity: .4;
                transition: $default-transition;
                cursor: not-allowed;
                pointer-events: none;
            }
        }

        &._hidden {
            display: none;
        }

        .itemWrapper {
            display: flex;
            align-items: flex-start;
            flex-direction: column;
        }

        .itemHead {
            display: flex;
            align-items: center;
            width: 100%;
        }

        .checkbox {
            margin-right: .8rem;
        }

        .itemBottom {
            margin-top: 1.6rem;
        }
    }
</style>
