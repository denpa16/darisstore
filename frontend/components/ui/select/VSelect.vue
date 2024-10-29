<script setup
        lang="ts"
>

/**
 * При работе с фильтрами и формами - позволяет выбирать одно или несколько значений.<br><br>
 *
 * У нас на проектах применяется принцип "фасетного фильтра", т.е.:<br>
 *
 * <strong>specs</strong> - диапазон всех доступных значений.<br>
 * <strong>facets</strong> - значения, которые доступны после передачи параметров из
 * <strong>value</strong>.<br><br>
 *
 * <a href="https://habr.com/ru/post/517074/" target="_blank">
 *     Подробннее про работу фасетных фильтров
 * </a>
 *
 * @version 1.1.0
 * @displayName VSelect
 */

// #region Imports
// Vue
import { computed, defineAsyncComponent, ref, useCssModule } from 'vue';
import { onClickOutside, useScrollLock } from '@vueuse/core';

// Types
import useSelect from '@idaproject/core/composables/ui/useSelect';
import type { VSelectProps } from './types';
import { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils'; // Components
import type { ChoiceLabel, ChoiceValue } from '~/types/filter';
import { ColorsEnum, SizeEnum, ThemeEnum } from '@/types/ui/type.ts';

// Components
const VScrollBox = defineAsyncComponent(() => import('~/components/ui/scrollbox/VScrollBox.vue'));
const VSelectOption = defineAsyncComponent(() => import('~/components/ui/select/VSelectOption.vue'));
// #endregion

// #region Props
const {
    name,
    specs,
    facets,
    modelValue = null,
    size = SizeEnum.medium,
    theme = ThemeEnum.light,
    color = ColorsEnum.primary,
    valueName = choiceValueKey,
    labelName = choiceLabelKey,
    placeholder = 'Все',
    resetLabel = 'Все',
    multiple = false,
    hideSelected,
    hideFiltered,
    disabled,
    required,
    prefixIcon,
    info,
    label,
    msg,
    infoRight,
    error,
    onlyOptions,
    hasInner,
    animationListKey,
    innerName,
    innerValue = null,
    innerMultiple,
    innerResetLabel,
    mobileModal = false,
    innerFiltersOuter,
    absoluteHint = true,
} = defineProps<VSelectProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'update:modelValue': [value: ChoiceValue | ChoiceValue[] | Record<ChoiceLabel, ChoiceValue | ChoiceValue[]>],
    focus: [],
    blur: [],
    'click-outside': [],
}>();
// #endregion

// #region Data
const el = document?.body;
const isLocked = useScrollLock(el);
const $style = useCssModule();
const vSelectRef = ref(null);
const inputHovering = ref<boolean>(false);

const {
    optionList,
    isDisabled,
    selectedOptions,
    selectedLabel,
    isFocused,
    isOpened,
    highlightIndex,
    inputRef,
    lazyValue,
    initLazyValue,
    onOptionSelect,
    onSetInner,
    onEnterPress,
    handleNavigateOptions,
    checkInner,
    handleToggleMenu,
    onBlur,
    onFocus,
} = useSelect(emit, name, toRef(() => disabled), toRef(() => specs), toRef(() => facets), valueName, labelName, toRef(() => modelValue), hideSelected, required, resetLabel, multiple, hideFiltered, placeholder, hasInner, toRef(() => innerValue), innerName, innerFiltersOuter, innerMultiple);
// #endregion

// #region Computed
const labelString = computed(() => required ? label + '<span>*</span>' : label);


const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${color}`]]: color,
        [$style[`_${size}`]]: size,
        [$style._focused]: isFocused.value,
        [$style._opened]: isOpened.value,
        [$style._disabled]: isDisabled.value,
        [$style._multiple]: multiple,
        [$style._error]: error,
        [$style._empty]: !selectedOptions.value.length,
        [$style._onlyOptions]: onlyOptions,
        [$style._mobileModal]: mobileModal,
    },
]);
// #endregion

// #region Lifecycle
checkInner();
initLazyValue();
onClickOutside(vSelectRef, () => onClickOutsideCallback());
// #endregion

// #region Methods
/**
 * Вызывается в тот момент, когда пользовать
 * сделал клик за пределы вызываемого селектором окна
 * @public
 */
function onClickOutsideCallback() {
    onBlur();

    /**
     * Эмитит в тот момент, когда пользовать
     * сделал клик за пределы вызываемого селектором окна
     * @event click-outside
     */
    emit('click-outside');
}

function disablePageScroll() {
    isLocked.value = true;
}

function enablePageScroll() {
    isLocked.value = false;
}

// #endregion
</script>

<template>
    <div
        ref="vSelectRef"
        :class="[$style.VSelect, classList]"
    >
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
                :class="[$style.icon, $style._label]"
                :text="info"
                @click.stop=""
            >
                <template #activator>
                    <VIcon name="information" />
                </template>
            </VTooltip>
        </div>

        <div
            v-if="!onlyOptions"
            :class="$style.field"
            @click.stop="handleToggleMenu"
        >
            <VIcon
                v-if="prefixIcon"
                :class="[$style.icon, $style._prefix]"
                :name="prefixIcon"
            />

            <input
                v-if="theme !== 'clear'"
                ref="inputRef"
                :class="$style.nativeInput"
                type="text"
                :value="selectedLabel"
                :disabled="isDisabled"
                :readonly="true"
                :data-test-id="name"
                @focus="onFocus"
                @keydown.down.stop.prevent="handleNavigateOptions('down')"
                @keydown.up.stop.prevent="handleNavigateOptions('up')"
                @keydown.enter.prevent="onEnterPress"
                @keydown.esc="isOpened = false"
                @keydown.tab="onBlur"
                @mouseenter="inputHovering = true"
                @mouseleave="inputHovering = false"
            />

            <div
                v-else
                :class="$style.textInput"
            >
                {{ selectedLabel }}
            </div>

            <VTooltip
                v-if="infoRight"
                :class="[$style.icon, $style._suffix]"
                :text="infoRight"
                @click.stop
            >
                <template #activator>
                    <VIcon name="information" />
                </template>
            </VTooltip>

            <VIcon
                :class="$style.arrow"
                name="arrow-down"
            />
        </div>

        <transition name="dropdown">
            <div
                v-if="isOpened || onlyOptions"
                :class="$style.dropdown"
            >
                <VScrollBox
                    resizable
                    :class="$style.scrollbox"
                >
                    <Transition
                        name="fade"
                        mode="out-in"
                    >
                        <div :key="animationListKey">
                            <VSelectOption
                                v-for="(option, index) in optionList"
                                :key="`${index}_${option[valueName]}`"
                                :option="option"
                                :value="lazyValue"
                                :value-name="valueName"
                                :label-name="labelName"
                                :size="size"
                                :theme="theme"
                                :is-highlighted="highlightIndex === index"
                                :multiple="multiple"
                                :has-inner="hasInner"
                                :inner-value="innerValue"
                                :inner-multiple="innerMultiple"
                                :inner-reset-label="innerResetLabel"
                                :next-selected="option.nextSelected"
                                @mouseenter="highlightIndex = index"
                                @mouseleave="highlightIndex = -1 "
                                @click="onOptionSelect"
                                @set-inner="onSetInner"
                            >
                                <slot
                                    name="option-content"
                                    :option="option"
                                >
                                </slot>
                            </VSelectOption>
                        </div>
                    </Transition>
                </VScrollBox>
            </div>
        </transition>

        <transition name="fade-fast">
            <InputHint
                v-if="msg && !isOpened"
                :theme="error ? 'alert' : theme"
                :absolute="absoluteHint"
                :disabled="disabled"
            >
                {{ msg }}
            </InputHint>
        </transition>

        <transition
            name="fade-fast-mobile"
            @before-enter="disablePageScroll()"
            @before-leave="enablePageScroll()"
        >
            <div
                v-if="mobileModal && isOpened"
                :class="$style.modal"
            >
                <VFilterModal
                    :title="label"
                    :btn-visible="false"
                    @back="onClickOutsideCallback"
                >
                    <VScrollBox
                        resizable
                        :class="$style.scrollbox"
                    >
                        <transition
                            name="fade"
                            mode="out-in"
                        >
                            <div
                                :key="animationListKey"
                                :class="$style.list"
                            >
                                <VSelectOption
                                    v-for="(option, index) in optionList"
                                    :key="`${index}_${option[valueName]}`"
                                    :option="option"
                                    :value="lazyValue"
                                    :value-name="valueName"
                                    :label-name="labelName"
                                    size="pre-medium"
                                    :theme="theme"
                                    :is-highlighted="highlightIndex === index"
                                    :multiple="multiple"
                                    :has-inner="hasInner"
                                    :inner-value="innerValue"
                                    :inner-multiple="innerMultiple"
                                    :inner-reset-label="innerResetLabel"
                                    :has-radio="!multiple"
                                    @mouseenter="highlightIndex = index"
                                    @mouseleave="highlightIndex = -1 "
                                    @click="onOptionSelect"
                                    @set-inner="onSetInner"
                                >
                                    <slot
                                        name="option-content"
                                        :option="option"
                                    >
                                    </slot>
                                </VSelectOption>
                            </div>
                        </transition>
                    </VScrollBox>
                </VFilterModal>
            </div>
        </transition>
    </div>
</template>

<style lang="scss"
       module
>
    $active-color: $primary-100;

    .VSelect {
        position: relative;
        user-select: none;

        /* Sizes */
        &._medium {
            .label {
                @include text(l3);

                display: flex;
                align-items: center;
                padding-bottom: 1.2rem;
            }

            .field {
                display: flex;
                align-items: center;
                height: 4.8rem;
                padding: 0 1.6rem;
            }

            .icon {
                &._prefix {
                    margin-right: .8rem;
                }

                &._suffix {
                    margin-right: 2.4rem;
                    margin-left: .8rem;
                }

                &._label {
                    margin-left: .6rem;
                }
            }

            .textInput,
            input.nativeInput {
                @include text(l1u);

                padding-right: 2.4rem;
                line-height: 1;

                @include respond-to(tablet) {
                    font-size: 16px;
                }
            }

            .arrow {
                right: 1.6rem;
            }

            .dropdown {
                top: calc(100%);
            }
        }

        /* Themes */
        &._light {
            &._primary {
                .label {
                    color: $base-600;

                    span {
                        color: $primary-900;
                    }
                }

                .icon {
                    color: $base-200;
                }

                input.nativeInput {
                    color: $base-500;
                    transition: color $default-transition;
                }

                .field {
                    border: 1px solid $base-200;
                    transition: border-color $default-transition;

                    @include hover {
                        border-color: $base-400;

                        input.nativeInput {
                            color: $base-900;
                        }
                    }
                }

                .arrow {
                    color: $base-900;
                }

                .dropdown {
                    background: $base-0;
                    color: $base-600;
                }

                &._disabled {
                    .field {
                        border-color: $base-100;
                    }

                    input.nativeInput {
                        color: $base-200;
                        -webkit-text-fill-color: $base-200;
                        opacity: 1;
                    }

                    .icon,
                    .arrow {
                        color: $base-100;
                    }
                }

                &._opened {
                    .field {
                        border-color: $base-400;

                        @include hover {
                            border-color: $base-600;
                        }
                    }
                }
            }
        }

        &._clear {
            .label {
                display: none;
            }

            .icon {
                &._prefix {
                    color: $base-200;
                }

                &._suffix,
                &._label {
                    display: none;
                }
            }

            .field {
                padding: 0;

                @include hover {
                    .textInput {
                        color: $base-600;
                    }
                }
            }

            .textInput {
                color: $base-500;
                transition: color $default-transition;
            }

            .arrow {
                right: 0;
            }

            .dropdown {
                top: calc(100% + 1.2rem);
                width: fit-content;
                max-width: 28rem;
            }

            &._disabled {
                .textInput {
                    color: $base-200;
                }

                .icon,
                .arrow {
                    color: $base-100;
                }
            }
        }

        /* Modificators */
        &._opened {
            .arrow {
                transform: rotate(180deg) translateY(50%);
            }
        }

        &._disabled {
            cursor: not-allowed;

            .field,
            .icon {
                pointer-events: none;
            }
        }

        &._empty {
            input.nativeInput {
                color: $base-400;
            }
        }

        &._onlyOptions {
            .dropdown {
                position: relative;
                top: 0;
                left: 0;
                box-shadow: none;

                .scrollbox {
                    max-height: none;
                }
            }
        }

        &._mobileModal {
            .dropdown {
                @include respond-to(tablet) {
                    display: none;
                }
            }
        }
    }

    .field {
        position: relative;
        width: 100%;
        cursor: pointer;
    }

    .icon {
        position: relative;
        z-index: 5;
        flex-shrink: 0;
    }

    .arrow {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        transition: all .3s;
        cursor: pointer;
    }

    .dropdown {
        position: absolute;
        top: calc(100% + 1.2rem);
        left: 0;
        z-index: 10;
        display: block;
        width: 100%;
        padding: .4rem;
        background: $base-0;
        transform: translate3d(0, 0, 0);
        transition: opacity .2s ease, transform .2s ease;
        box-shadow: 0 4px 38px 0 rgb(0 0 0 / 8%);

        .scrollbox {
            max-height: 28.8rem;
        }
    }

    input.nativeInput {
        overflow: hidden;
        display: inline-block;
        width: 100%;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-weight: 500;
        transition: color $default-transition, opacity $default-transition, background $default-transition;
        cursor: pointer;

        &::selection {
            background: transparent;
        }
    }

    .modal {
        display: none;

        @include respond-to(tablet) {
            display: block;
        }
    }

    .list {
        @include respond-to(tablet) {
            padding: 2rem 1.2rem;
        }
    }
</style>
