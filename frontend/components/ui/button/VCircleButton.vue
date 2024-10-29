<script
    setup
    lang="ts"
>

/**
 * Кастомная альтернатива тега button в стандартном html<br>
 * На проектах, обычно, имеет несколько цветов, форм и состояний.<br><br>
 * Область применения: ссылка, изменения состояния, вызов методов.
 *
 * @displayName VCircleButton
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
// #endregion

// #region Interfaces
export interface ICircleButtonProps {
    /**
     * Определяет тег компонента
     */
    tag?: string;
    target?: string;
    /**
     * Название иконки
     */
    icon: string;
    /**
     * Определяет классы, которые будут модифицировать размер
     *  @values small, medium, large
     */
    size?: Extract<TSize, 'large' | 'medium' | 'small'>,
    /**
     * Определяет классы, которые будут модифицировать тему
     * @values primary, secondary
     */
    theme?: TTheme,
    /**
     * Определяет классы, которые будут модифицировать цвет
     * @values primary, secondary, tertiary
     */
    color?: TColor
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
    name?: string,
}

// #endregion

// #region Props
const props = withDefaults(defineProps<ICircleButtonProps>(), {
    tag: 'button',
    size: SizeEnum.medium,
    theme: ThemeEnum.light,
    color: ColorsEnum.primary,
    target: '',
    name: '',
    icon: 'arrow-left',
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
} = useButton(emit, props.target, props.disabled);
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
    },
]);

const component = computed(() => {
    if (props.tag) {
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
        <transition
            name="fade-fast"
            mode="out-in"
        >
            <div
                v-if="loading"
                :class="$style.loader"
            >
                <VLoading
                    :theme="loaderTheme"
                    :size="loaderSize"
                />
            </div>
        </transition>
        <div :class="$style.wrapper">
            <VIcon
                :name="icon"
                size="custom"
                :class="$style.icon"
            />
        </div>
        <div :class="$style.wrapperDuplicate">
            <VIcon
                :name="icon"
                size="custom"
                :class="$style.icon"
            />
        </div>
    </component>
</template>

<style
    lang="scss"
    module
>
    /* Colors */

    .VButton {
        --size: auto;

        position: relative;
        overflow: hidden;
        display: inline-block;
        width: var(--size);
        height: var(--size);
        border-radius: 100%;
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

            .icon {
                width: 1.4rem;
                height: 1.4rem;
            }
        }

        &._medium {
            --size: 4rem;

            .icon {
                width: 1.8rem;
                height: 1.8rem;
            }
        }

        &._large {
            --size: 4.8rem;

            .icon {
                width: 2rem;
                height: 2rem;
            }
        }

        /* Themes */
        &._light {
            &._primary {
                border-color: $base-900;

                &:before {
                    background-color: $base-900;
                }

                .icon {
                    color: $base-0;
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

                .icon {
                    color: $base-900;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $base-50;
                    }

                    .icon {
                        color: $opacity-main-40;
                    }
                }
            }

            &._tertiary {
                border-color: $base-900;

                &:before {
                    background-color: $base-0;
                }

                .icon {
                    color: $base-900;
                }

                &._disabled {
                    border-color: $opacity-main-40;

                    .icon {
                        color: $opacity-main-40;
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

                .icon {
                    color: $base-900;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $opacity-white-20;
                    }

                    .icon {
                        color: $opacity-white-40;
                    }
                }
            }

            &._secondary {
                border-color: $opacity-white-20;

                &:before {
                    background-color: $opacity-white-20;
                }

                .icon {
                    color: $base-0;
                }

                &._disabled {
                    &:before,
                    &:after {
                        background-color: $opacity-white-10;
                    }

                    .icon {
                        color: $opacity-white-40;
                    }
                }
            }

            &._tertiary {
                border-color: $opacity-white-40;

                &:before {
                    background-color: $base-900;
                }

                .icon {
                    color: $base-0;
                }

                &._disabled {
                    border-color: $opacity-white-40;

                    .icon {
                        color: $opacity-white-40;
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

                .icon {
                    color: $base-0;
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

                .icon {
                    color: $base-0;
                }
            }
        }

        &._loading {
            pointer-events: none;

            .icon {
                opacity: 0;
            }
        }

        &._disabled {
            cursor: not-allowed;
        }
    }

    .wrapperDuplicate,
    .wrapper {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        height: 100%;
        transition: opacity $default-transition, transform $default-transition;
    }

    .icon {
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: 2;
        transform: translate(-50%, -50%);
        transition: $default-transition;
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
