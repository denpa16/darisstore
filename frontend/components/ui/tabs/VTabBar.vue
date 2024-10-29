<script setup
        lang="ts"
>
// #region Imports
import type { VTabBarProps } from './types';
import { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils';
import type { Choice, ChoiceLabel, ChoiceValue } from '~/types/filter';
import { SizeEnum, ThemeEnum } from '@/types/ui/type.ts';
// #endregion

// #region Props
const {
    name,
    tag = 'ul',
    childTag = 'li',
    specs,
    facets,
    valueName = choiceValueKey,
    labelName = choiceLabelKey,
    modelValue = null,
    slider = false,
    theme = ThemeEnum.light,
    size = SizeEnum.medium,
    close = false,
    multiple,
    extraPad,
    flexWrap,
    fullWidth,
    fullWidthWrapper,
    resetLabel,
    required,
    border = false,
    hasShadow = false,
} = defineProps<VTabBarProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'update:modelValue': [value: (ChoiceValue | ChoiceValue[]) | Record<ChoiceLabel, ChoiceValue | ChoiceValue[]>],
    'tab-enter': [event: MouseEvent, value: Choice],
    'tab-leave': [event: MouseEvent, value: Choice],
    'tab-info-click': [value: Choice],
    'tab-bar-active-tab-width': [value: number],
    'tab-bar-active-tab-offset': [value: number],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const lazyValue = ref<ChoiceValue | ChoiceValue[]>(multiple ? [] : null);
const bgSliderRef = ref<HTMLElement | null>(null);
const tabsRef = ref([]);
const resizeObserver = ref<ResizeObserver | null>(null);
const tabBarRef = ref<HTMLElement | null>(null);

initLazyValue();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${size}`]]: size,
        [$style._close]: close,
        [$style._slider]: slider,
        [$style._flexWrap]: flexWrap,
        [$style._fullWidth]: fullWidth,
        [$style._fullWidthWrapper]: fullWidthWrapper,
        [$style._noSelected]: !modelValue && !resetLabel,
        [$style._shadow]: hasShadow,
    },
]);

const optionsList = computed(() => {
    const specsList = [...specs];

    if (!required && resetLabel) {
        specsList.unshift({
            [labelName]: resetLabel,
            [valueName]: null,
        });
    }

    return specsList;
});

const currentIndex = computed(() => {
    if (multiple || !(modelValue || typeof modelValue === 'boolean' || modelValue === 0)) {
        return null;
    }

    return optionsList.value.findIndex(el => el[valueName] === modelValue);
});
// #endregion

// #region Watch
watch(() => close, () => {
    nextTick(calcBg);
});

watch(() => size, () => {
    nextTick(calcBg);
});

watch(() => slider, (val: boolean) => {
    if (val) {
        nextTick(calcBg);
    }
});

watch(() => modelValue, () => {
    if (multiple && !modelValue) {
        lazyValue.value = [];
    } else {
        lazyValue.value = modelValue;
    }

    calcBg();
});
// #endregion

// #region Lifecycle
onMounted(() => {
    calcBg();

    if (slider) {
        resizeObserver.value = new ResizeObserver(calcBg);
        resizeObserver.value.observe(tabBarRef.value as HTMLElement);
    }
});

onUnmounted(() => {
    resizeObserver.value?.disconnect();
});
// #endregion

// #region Methods
function initLazyValue() {
    if (multiple) {
        if (Array.isArray(modelValue)) {
            lazyValue.value = [...modelValue];
        } else if (modelValue || typeof modelValue === 'boolean' || modelValue === 0) {
            lazyValue.value = [modelValue];
        } else {
            lazyValue.value = [];
        }
    } else {
        lazyValue.value = modelValue;
    }
}

async function calcBg() {
    if (!slider || multiple) {
        return;
    }

    await nextTick();
    bgSliderWidth(currentIndex.value);
    bgSliderOffset(currentIndex.value);
}


function onTabChange(val: ChoiceValue) {
    if (facets && !facets.includes(val) && val !== null) {
        return;
    }

    let emitVal;

    if (val === null) {
        emitVal = multiple ? [] : null;
    } else if (multiple) {
        (lazyValue.value as ChoiceValue[]).includes(val)
            ? (lazyValue.value as ChoiceValue[]).splice((lazyValue.value as ChoiceValue[]).indexOf(val), 1)
            : (lazyValue.value as ChoiceValue[]).push(val);

        emitVal = [...(lazyValue.value as ChoiceValue[])];
    } else {
        emitVal = val === lazyValue.value && !required ? null : val;
    }

    emit('update:modelValue', name ? { [name]: emitVal } : emitVal);
    calcBg();
}

function bgSliderWidth(ind: number | null) {
    const tabWidth = tabsRef.value[ind || 0]?.$el.getBoundingClientRect()?.width;
    if (bgSliderRef.value?.style) {
        bgSliderRef.value.style.width = `${tabWidth}px`;
    }
    emit('tab-bar-active-tab-width', tabWidth);
}

function bgSliderOffset(ind: number | null) {
    const offset = tabsRef.value[ind || 0]?.$el.offsetLeft;
    if (bgSliderRef.value?.style) {
        bgSliderRef.value.style.left = `${offset}px`;
    }
    emit('tab-bar-active-tab-offset', offset);
}

// #endregion
</script>

<template>
    <div
        ref="tabBarRef"
        :class="[$style.VTabBar, ...classList]"
        :data-test-id="name"
    >
        <div :class="$style.wrapper">
            <div
                v-show="slider"
                ref="bgSliderRef"
                :class="['bg-slider', $style.slider]"
            >
            </div>
            <div
                v-if="border"
                :class="[$style.border,'border']"
            >
            </div>

            <component
                :is="tag"
                :class="$style.list"
            >
                <VTab
                    v-for="(tab, tabInd) in optionsList"
                    :key="`${tab[valueName]}_${tabInd}`"
                    ref="tabsRef"
                    :tag="childTag"
                    :tab="tab"
                    :theme="theme"
                    :size="size"
                    :close="close"
                    :slider="slider"
                    :active=" (
                        (multiple && ((lazyValue as ChoiceValue[]).includes(tab[valueName]) || !(lazyValue as ChoiceValue[]).length && tab[valueName] === null))
                        || (lazyValue === tab[valueName])
                        || (lazyValue === null && tab[valueName] === null)
                    )"
                    :disabled="facets && !facets.includes(tab[valueName]) && tab[valueName] !== null"
                    :extra-pad="extraPad"
                    :class="$style.tab"
                    @click="onTabChange(tab[valueName])"
                    @tab-enter="$emit('tab-enter', $event, tab)"
                    @tab-leave="$emit('tab-leave', $event, tab)"
                >
                    <slot
                        name="tab-content"
                        :tab="tab"
                    >
                        {{ tab[labelName] }}
                    </slot>
                </VTab>
            </component>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    $primary: $primary-100;

    .VTabBar {
        position: relative;
        display: flex;
        user-select: none;

        /* Sizes */
        &._small {
            .list {
                gap: 4.8rem;

                @include respond-to(tablet) {
                    gap: 1.6rem;
                }
            }

            &._close {
                .list {
                    gap: .4rem;
                }
            }
        }

        &._medium {
            .list {
                gap: 4.8rem;
            }

            &._close {
                .list {
                    gap: .8rem;
                }
            }
        }

        /* Modificators */

        &._flexWrap {
            .list {
                flex-wrap: wrap;
            }
        }

        &._fullWidth {
            width: 100%;

            .wrapper,
            .list {
                width: 100%;
            }

            .tab {
                flex-grow: 1;
                flex-basis: 100%;
                min-width: auto;
            }
        }

        &._fullWidthWrapper {
            .wrapper,
            .list {
                width: 100%;
            }
        }

        &._close {
            &._slider {
                padding: .4rem;
                border-radius: 100rem;
                background-color: $base-100;

                .slider {
                    border-radius: 100rem;
                    background-color: $base-0;
                    box-shadow: 1px 1px 4px 0 rgb(21 22 24 / 8%);
                }
            }

            .slider {
                height: 100%;
                border-radius: .6rem;
            }
        }

        &._noSelected {
            .slider {
                opacity: 0;
            }
        }

        &._shadow {
            &._slider {
                background-color: transparent;

                .slider {
                    left: 0;

                    &:after {
                        content: "";
                        position: absolute;
                        inset: .4rem .4rem .4rem .4rem;
                    }
                }
            }
        }
    }

    .wrapper,
    .list {
        position: relative;
        display: flex;
    }

    .border {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: .1rem;
        background-color: $base-200;
        transition: .3s;
    }

    .slider {
        position: absolute;
        bottom: 0;
        left: 0;
        min-width: 1rem;
        height: .2rem;
        background-color: $base-600;
        transition: $default-transition;
    }
</style>
