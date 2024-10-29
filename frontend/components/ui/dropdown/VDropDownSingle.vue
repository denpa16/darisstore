<script setup lang="ts">
// #region Imports
// Vue
import { onClickOutside, useScrollLock } from '@vueuse/core';
// Utils
// Types
import { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils';
import type { VDropDownSingleProps } from './types.ts';
import type { Choice, ChoiceLabel, ChoiceValue } from '~/types/filter';
import { ColorsEnum, SizeEnum, ThemeEnum } from '@/types/ui/type.ts';
// #endregion

// #region Props
const props = withDefaults(defineProps<VDropDownSingleProps>(), {
    value: null,
    theme: ThemeEnum.light,
    color: ColorsEnum.primary,
    size: SizeEnum.medium,
    additionalLabelFilter: val => val,
    sizeIconLeft: SizeEnum.medium,
    sizeIconRight: SizeEnum.medium,
    iconLeft: '',
    iconRight: '',
});
// #endregion

// #region Emits
const emit = defineEmits<{
    'update:modelValue': [value: (ChoiceValue | ChoiceValue[]) | Record<ChoiceLabel, ChoiceValue | ChoiceValue[]>],
}>();
// #endregion

// #region Data
const el = document?.body;
const isLocked = useScrollLock(el);
const $style = useCssModule();
const isVisibleList = ref<boolean>(false);
const dropdown = ref<HTMLElement | null>(null);
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.theme,
        [$style[`_${props.color}`]]: props.color,
        [$style._disabled]: props.disabled,
    },
]);

const optionList = computed(() => {
    if (!props.facets) {
        return props.specs;
    }

    return props.specs.filter(opt => opt[choiceValueKey] !== null && props.facets?.includes(opt[choiceValueKey] as string | number));
});

const activeOption = computed(() => optionList.value?.find(el => el[choiceValueKey] === props.value));
// #endregion

// #region Methods
const lockScroll = () => {
    isLocked.value = Boolean(isVisibleList.value);
};
const toggleList = () => {
    isVisibleList.value = !isVisibleList.value;
    lockScroll();
};

const mouseOpenList = () => {
    isVisibleList.value = true;
};

const mouseCloseList = () => {
    isVisibleList.value = false;
};

const closeList = () => {
    isVisibleList.value = false;
    lockScroll();
};

const clickItem = (item: Choice) => {
    if (props.value !== item[choiceValueKey]) {
        emit('update:modelValue', name ? { [name]: item[choiceValueKey] } : item[choiceValueKey]);
    }

    isVisibleList.value = false;
};
// #endregion

onClickOutside(dropdown, () => closeList());
</script>

<template>
    <div
        ref="dropdown"
        :class="[$style.VDropDownSingle, classList]"
        @mouseenter="mouseOpenList"
        @mouseleave="mouseCloseList"
    >
        <VButton
            :size="size"
            round
            border
            :full-width="isFullWidth"
            :class="$style.trigger"
            @click.stop="toggleList"
        >
            <VIcon
                v-if="iconLeft"
                :class="$style.iconLeft"
                :name="iconLeft"
                :size="sizeIconLeft"
            />
            <span :class="$style.label">
                {{
                    label
                }}<span :class="$style.additionalLabel">{{
                    additionalLabelFilter(activeOption?.[choiceValueKey] ? (activeOption[choiceLabelKey] as string) : '')
                }}</span>
            </span>
            <VIcon
                v-if="iconRight"
                :class="$style.iconRight"
                :name="iconRight"
                :size="sizeIconRight"
            />
        </VButton>

        <div
            :class="[$style.container, {[$style._visible]: isVisibleList}]"
            @click="closeList"
        >
            <div :class="[$style.listWrapper, {[$style._visible]: isVisibleList}]">
                <div :class="$style.closeList">
                    {{ label }}

                    <VButton
                        :class="$style.closeBtn"
                        round
                        border
                        equal
                        @close="closeList"
                    >
                        <VIcon
                            name="mock-close"
                            size="sLarge"
                        />
                    </VButton>
                </div>
                <VScrollBox
                    :class="$style.scrollBox"
                    resizable
                >
                    <ul :class="$style.list">
                        <li
                            v-for="item in optionList"
                            :key="`item_${item[choiceValueKey]}`"
                            :class="[$style.item, {[$style._active]: value === item[choiceValueKey]}]"
                            @click.stop="clickItem(item)"
                        >
                            {{ item[choiceLabelKey] }}
                            <span :class="$style.radio"></span>
                        </li>
                    </ul>
                </VScrollBox>
            </div>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    .VDropDownSingle {
        position: relative;

        &:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: calc(100% + 1.2rem);
            cursor: pointer;

            @include respond-to(tablet) {
                content: none;
            }
        }

        &._light {
            &._primary {
                .container {
                    @include respond-to(tablet) {
                        background-color: $opacity-main-40;
                    }
                }

                .closeList {
                    &:after {
                        background-color: $base-200;
                    }
                }

                .listWrapper {
                    box-shadow: $box-shadow-default;
                    background-color: $base-0;
                }

                .item {
                    &:not(:last-child) {
                        border-bottom: 1px solid $base-200;
                    }

                    @include hover {
                        background-color: $base-100;
                    }

                    &._active {
                        border-color: transparent;
                        background-color: $base-100;

                        .radio {
                            border-color: $base-600;
                        }
                    }
                }

                .radio {
                    border: 2px solid $base-400;

                    &:before {
                        background-color: $base-600;
                    }
                }
            }
        }
    }

    .trigger {
        position: relative;
    }

    .iconLeft {
        margin-right: .8rem;
    }

    .iconRight {
        margin-left: .8rem;
    }

    .additionalLabel {
        @include respond-to(tablet) {
            display: none;
        }
    }

    .container {
        @include respond-to(tablet) {
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
            display: flex;
            align-items: flex-end;
            width: 100%;
            height: 100%;
            padding: 0;
            opacity: 0;
            pointer-events: none;
            transform: translateY(200%);
            transition: opacity $default-transition;

            &._visible {
                opacity: 1;
                pointer-events: all;
                transform: translateY(0);
            }
        }
    }

    .closeList {
        @include text(l2-regular);

        position: relative;
        display: none;
        align-items: center;
        justify-content: space-between;
        padding: 1.2rem 2rem;

        &:after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 1px;
        }

        @include respond-to(tablet) {
            display: flex;
        }
    }

    .closeBtn {
        margin-left: 1.2rem;
    }

    .scrollBox {
        max-height: 46rem;

        @include respond-to(tablet) {
            max-height: calc(100dvh - 10rem);
        }
    }

    .listWrapper {
        position: absolute;
        top: calc(100% + 1.2rem);
        left: 0;
        z-index: 3;
        width: 100%;
        min-width: 30rem;
        border-radius: 1.2rem;
        opacity: 0;
        transform: translateY(10px);
        pointer-events: none;
        transition: opacity $default-transition, transform $default-transition;

        &._visible {
            opacity: 1;
            transform: translateY(0);
            pointer-events: all;

            @include respond-to(tablet) {
                transform: translate(-50%, 0);
            }
        }

        @include respond-to(tablet) {
            position: fixed;
            top: auto;
            bottom: 0;
            left: 50%;
            z-index: 10;
            width: 100%;
            max-width: 47.8rem;
            transform: translate(-50%, 200%);
        }

        @include respond-to(mobile) {
            max-width: 100%;
            border-bottom-left-radius: initial;
            border-bottom-right-radius: initial;
        }
    }

    .list {
        padding: .8rem;
    }

    .item {
        @include text(l3-regular);

        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.8rem 1.2rem;
        cursor: pointer;

        @include hover {
            border-radius: .8rem;
        }

        &._active {
            border-radius: .8rem;

            .radio {
                &:before {
                    opacity: 1;
                }
            }
        }
    }

    .radio {
        position: relative;
        flex-shrink: 0;
        width: 2rem;
        height: 2rem;
        margin-left: 1rem;
        border-radius: 50%;
        transition: border-color $default-transition;

        &:before {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            width: 1rem;
            height: 1rem;
            border-radius: 50%;
            opacity: 0;
            transform: translate(-50%, -50%);
            transition: opacity $default-transition;
        }
    }
</style>
