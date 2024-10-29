<script setup lang="ts">

/**
 * Кастомная альтернатива тега button в стандартном html<br>
 * На проектах, обычно, имеет несколько цветов, форм и состояний.<br><br>
 * Область применения: ссылка, изменения состояния, вызов методов.
 *
 * @displayName VButton
 */

// #region Imports
import useButton from '@idaproject/core/composables/ui/useButton';
import {
    ColorsEnum,
    SizeEnum,
    type TColor,
    ThemeEnum,
    type TSize,
    type TTheme,
} from '@/types/ui/type.ts';
import type { TIconSize } from '@/components/ui/icon/types.ts';
// #endregion

// #region Interfaces
export interface IButtonProps {
    /**
     * Определяет тег компонента
     */
    tag?: string;
    /**
     * Ссылка как внутренняя (/project) так и внешняя (https://idaproject.com/about)
     */
    to?: string;
    /**
     * Определяет, где показать содержимое
     */
    target?: '' | '_blank' | '_self' | '_parent' | '_top';
    /**
     * Определяет классы, которые будут модифицировать размер
     *  @values small, medium, large
     */
    size?: Extract<TSize, 'large' | 'medium' | 'small'>;
    /**
     * Определяет классы, которые будут модифицировать тему
     * @values primary, secondary
     */
    theme?: TTheme;
    /**
     * Определяет классы, которые будут модифицировать цвет
     * @values primary, secondary, tertiary
     */
    color?: TColor;
    /**
     * Активное состояние кнопки
     */
    active?: boolean;
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean;
    /**
     * Модификатор состояния загрузки на кнопке
     */
    loading?: boolean;
    /**
     * Модификатор выравнивания контента внутри label
     */
    justifyBetween?: boolean,
    /**
     * Модификатор растягивания кнопки по всей ширине
     */
    fullWidth?: boolean,
    name?: string,
    /**
     * Ионка слева
     */
    leftIconName?: string,
    /**
     * Ионка справа
     */
    rightIconName?: string,
    /**
     * Размер иконки
     */
    iconSize?: TIconSize,
}

// #endregion

// #region Props
const props = withDefaults(defineProps<IButtonProps>(), {
    tag: 'button',
    size: SizeEnum.medium,
    theme: ThemeEnum.light,
    color: ColorsEnum.primary,
    target: '',
    name: '',
    leftIconName: '',
    rightIconName: '',
    iconSize: SizeEnum.medium,
    to: '',
});
// #endregion

// #region Emits
const emit = defineEmits<{
    /**
     * Event click.
     */
    click: [value: MouseEvent],
    mouseenter: [value: MouseEvent],
    mouseleave: [value: MouseEvent],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const {
    buttonAttrs,

    /**
     * Эмитит событие клика в родительский компонент
     * @param {Event} event - mouse event
     * @function onClick
     */
    onClick,
    /**
     * Эмитит событие клика в родительский компонент
     * @param {Event} event
     * @function onMouseEnter
     */
    onMouseEnter,
    /**
     * onMouseLeave
     * @param {event: MouseEvent} MouseEvent
     * @function
     */
    onMouseLeave,
} = useButton(emit, toRef(() => props.to), '', toRef(() => props.target), toRef(() => props.disabled));
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.theme,
        [$style[`_${props.color}`]]: props.color,
        [$style[`_${props.size}`]]: props.size,
        [$style._disabled]: props.disabled,
        [$style._active]: props.active,
        [$style._loading]: props.loading,
        [$style._justifyBetween]: props.justifyBetween,
        [$style._fullWidth]: props.fullWidth,
    },
]);

const component = computed(() => {
    if (props.to) {
        return resolveComponent('NuxtLink');
    } else if (props.tag) {
        return props.tag;
    } else {
        return 'button';
    }
});

const loaderSize = computed((): SizeEnum.medium | SizeEnum.small => props.size === SizeEnum.large ? SizeEnum.medium : SizeEnum.small);

const loaderTheme = computed((): TTheme => {
    if (props.theme === ThemeEnum.light && props.color === ColorsEnum.primary ||
        props.theme === ThemeEnum.dark && props.color === ColorsEnum.tertiary) {
        return ThemeEnum.light;
    }

    return ThemeEnum.dark;
});
// #endregion
</script>

<template>
    <component
        :is="component"
        :class="[$style.VButton, classList, 'vbutton']"
        :disabled="disabled"
        v-bind="buttonAttrs"
        :data-test-id="name"
        @click="onClick"
        @mouseenter="onMouseEnter"
        @mouseleave="onMouseLeave"
    >
        <!-- Лоадер -->
        <transition name="fade-fast" mode="out-in">
            <div
                v-if="loading"
                :class="$style.loader"
            >
                <VLoading :theme="loaderTheme" :size="loaderSize" />
            </div>
        </transition>
        <div :class="$style.wrapper">
            <VIcon
                v-if="leftIconName"
                :name="leftIconName"
                :size="iconSize"
                :class="$style.iconLeft"
            />

            <div
                v-if="$slots.default"
                :class="[$style.label, 'vbutton__label']"
            >

                <!-- @slot Контент внутри кнопки -->
                <slot></slot>
            </div>

            <div
                v-if="$slots.subLabel"
                :class="[$style.subLabel, 'vbutton__sublabel']"
            >

                <!-- @slot Доп контент внутри кнопки -->
                <slot name="subLabel"></slot>
            </div>

            <VIcon
                v-if="rightIconName"
                :name="rightIconName"
                :size="iconSize"
                :class="$style.iconRight"
            />
        </div>
        <div :class="$style.wrapperDuplicate">
            <VIcon
                v-if="leftIconName"
                :name="leftIconName"
                :size="iconSize"
                :class="$style.iconLeft"
            />

            <div
                v-if="$slots.default"
                :class="[$style.label, 'vbutton__label']"
            >

                <!-- @slot Контент внутри кнопки -->
                <slot></slot>
            </div>

            <div
                v-if="$slots.subLabel"
                :class="[$style.subLabel, 'vbutton__sublabel']"
            >

                <!-- @slot Доп контент внутри кнопки -->
                <slot name="subLabel"></slot>
            </div>

            <VIcon
                v-if="rightIconName"
                :name="rightIconName"
                :size="iconSize"
                :class="$style.iconRight"
            />
        </div>
    </component>
</template>

<style lang="scss"
       module
>
    /* Colors */

    .VButton {
        --size: auto;

        position: relative;
        overflow: hidden;
        display: inline-block;
        height: var(--size);
        border: 1px solid;
        outline: none;
        transition: color $default-transition, opacity $default-transition, background-color $default-transition, border-color $default-transition;
        cursor: pointer;
        user-select: none;

        &:after,
        &:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
            width: 100%;
            height: 100%;
        }

        &:after {
            background-color: $primary-900;
            transform: translateY(110%);
            transition: transform $default-transition;
        }

        /* Sizes */
        &._small {
            --size: 3.2rem;

            min-width: 3.2rem;

            .label {
                padding: 0 3rem;
            }
        }

        &._medium {
            --size: 4rem;

            min-width: 4rem;

            .label {
                padding: 0 3rem;
            }
        }

        &._large {
            --size: 4.8rem;

            min-width: 7.4rem;

            .label {
                padding: 0 5rem;
            }

            .label,
            .subLabel {
                @include text(l1u);
            }
        }

        /* Themes */
        &._light {
            &._primary {
                border-color: $base-900;

                &:before {
                    background-color: $base-900;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-0;
                }

                .subLabel {
                    color: $opacity-white-60;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $base-200;
                    }
                }
            }

            &._secondary {
                border-color: $base-75;

                &:before {
                    background-color: $base-75;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-900;
                }

                .subLabel {
                    border-left: 1px solid $opacity-main-20;
                    color: $opacity-white-40;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $base-50;
                    }

                    .iconLeft,
                    .iconRight,
                    .label {
                        color: $opacity-main-40;
                    }

                    .subLabel {
                        color: $opacity-main-20;
                    }
                }
            }

            &._tertiary {
                border-color: $base-900;

                &:before {
                    background-color: $base-0;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-900;
                }

                .subLabel {
                    border-left: 1px solid $opacity-main-20;
                    color: $opacity-main-40;
                }

                &._disabled {
                    border-color: $opacity-main-40;

                    .iconLeft,
                    .iconRight,
                    .label {
                        color: $opacity-main-40;
                    }

                    .subLabel {
                        color: $opacity-main-20;
                    }
                }
            }
        }

        &._dark {
            &._primary {
                border-color: $base-0;

                &:before {
                    background-color: $base-0;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-900;
                }

                .subLabel {
                    color: $opacity-main-60;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $opacity-white-20;
                    }

                    .iconLeft,
                    .iconRight,
                    .label {
                        color: $opacity-white-40;
                    }

                    .subLabel {
                        color: $opacity-white-20;
                    }
                }
            }

            &._secondary {
                border-color: $opacity-white-20;

                &:before {
                    background-color: $opacity-white-20;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-0;
                }

                .subLabel {
                    color: $opacity-white-60;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $opacity-white-10;
                    }

                    .iconLeft,
                    .iconRight,
                    .label {
                        color: $opacity-white-40;
                    }

                    .subLabel {
                        color: $opacity-white-20;
                    }
                }
            }

            &._tertiary {
                border-color: $opacity-white-40;

                &:before {
                    background-color: $base-900;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-0;
                }

                .subLabel {
                    color: $opacity-white-60;
                }

                &._disabled {
                    border-color: $opacity-white-40;

                    .iconLeft,
                    .iconRight,
                    .label {
                        color: $opacity-white-40;
                    }

                    .subLabel {
                        color: $opacity-white-20;
                    }
                }
            }
        }

        /* Hover */
        @include hover {
            &:not(._disabled) {
                border-color: $primary-900;

                .wrapper,
                .wrapperDuplicate {
                    transform: translateY(-100%);
                }

                &:after {
                    transform: translateY(0);
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-0;
                }

                .subLabel {
                    color: $opacity-white-60;
                }
            }
        }

        /* Modificators */
        &:is(._light, ._dark) {
            &:active,
            &._active {
                border-color: $primary-900;

                &:before {
                    background-color: $primary-900;
                }

                .iconLeft,
                .iconRight,
                .label {
                    color: $base-0;
                }

                .subLabel {
                    color: $opacity-white-60;
                }
            }
        }

        &._loading {
            pointer-events: none;

            .wrapper {
                opacity: 0;
            }
        }

        &._disabled {
            cursor: not-allowed;
        }

        &._fullWidth {
            width: 100%;
        }

        &._equal {
            width: var(--size);
            min-width: auto;
            height: var(--size);

            .label {
                justify-content: center;
                width: 100%;
                padding: 0;
            }
        }

        &._justifyBetween {
            .label {
                justify-content: space-between;
            }
        }
    }

    .wrapperDuplicate,
    .wrapper {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        height: 100%;
        gap: .8rem;
        transition: opacity $default-transition, transform $default-transition;
    }

    .label,
    .subLabel {
        @include text(l2u);

        width: 100%;
        white-space: nowrap;
        transition: color $default-transition;
    }

    .label {
        display: inline-flex;
        align-items: center;
        justify-content: center;

        svg {
            position: relative;
            display: inline-block;
            vertical-align: center;
        }
    }

    .subLabel {
        padding-left: .8rem;
        border-left: 1px solid $opacity-white-20;
    }

    .loader {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }
</style>
