<script setup lang="ts">
/**
 * Кастомная альтернатива компонента NuxtLink<br>
 * На проектах, обычно, имеет несколько цветов, форм и состояний.<br><br>
 * Область применения: ссылка.
 *
 * @version 1.0.1
 * @displayName VLink
 */

// #region Imports
import { resolveComponent } from 'vue';
import type { Props } from './types.ts';
// #endregion

// #region Props
const {
    tag = 'div',
    to,
    target,
    size = 'medium',
    theme = 'light',
    type,
    active,
    disabled,
    hasArrow,
    alwaysInteracting = false,
} = defineProps<Props>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${size}`]]: size,
        [$style[`_${type}`]]: type,
        [$style._active]: active,
        [$style._disabled]: disabled,
        [$style._alwaysInteracting]: alwaysInteracting,
    },
]);

const linkComponent = computed(() => {
    const isLink = !disabled && to;
    if (tag === 'button') {
        return {
            is: tag,
        };
    }

    return {
        is: isLink ? resolveComponent('NuxtLink') : 'div',
        to: isLink ? to : null,
    };
});
// #endregion

// #region Methods
// #endregion
</script>

<template>
    <component
        :is="linkComponent.is"
        :to="linkComponent.to"
        :class="[$style.VLink, classList]"
        :target="target"
    >
        <div
            v-if="$slots.default"
            :class="$style.label"
        >
            <span :class="$style.text">
                <!-- @slot Контент внутри ссылки -->
                <slot></slot>
            </span>
            <VIcon
                v-if="hasArrow"
                name="mock-arrow"
                size="custom"
            />
        </div>
    </component>
</template>

<style lang="scss" module>
    /* Colors */
    // Base
    $base-black: $base-600;
    $base-white: #fff;
    $base-hover: $base-600;
    $base-disabled: $base-400;
    $base-disabled-secondary: $base-500;

    .VLink {
        display: inline-flex;
        outline: none;
        transition: color $default-transition, opacity $default-transition, background-color $default-transition, border-color $default-transition;
        cursor: pointer;
        user-select: none;

        /* Sizes */
        &._small {
            @include text(l4-regular);

            .label {
                svg {
                    top: .2rem;
                }
            }
        }

        &._medium {
            @include text(l3-regular);
        }

        &._large {
            @include text(l2-regular);
        }

        /* Themes */
        &._light {
            &:after {
                background-color: $base-black;
            }

            .label {
                color: $base-black;

                span:after {
                    background-color: $base-black;
                }
            }

            &._active {
                &:after {
                    background-color: $base-hover;
                }

                .label {
                    color: $base-hover;

                    span:after {
                        background-color: $base-hover;
                        transform: scaleX(0) translateZ(0);
                    }
                }
            }

            &._disabled {
                &:after {
                    background-color: $base-disabled;
                }

                .label {
                    color: $base-disabled;

                    span:after {
                        background-color: $base-disabled;
                    }
                }
            }

            @include hover {
                &:not(._disabled) {
                    &:after {
                        background-color: $base-400;
                    }

                    .label {
                        color: $base-400;

                        span:after {
                            background-color: $base-400;
                            transform: scaleX(0) translateZ(0);
                        }
                    }
                }
            }
        }

        &._dark {
            &:after {
                background-color: $base-white;
            }

            .label {
                color: $base-white;

                span:after {
                    background-color: $base-white;
                }
            }

            &._active {
                &:after {
                    background-color: $base-white;
                }

                .label {
                    color: $base-white;

                    span:after {
                        background-color: $base-white;
                        transform: scaleX(0) translateZ(0);
                    }
                }
            }

            &._disabled {
                &:after {
                    background-color: rgba($base-white, .4);
                }

                .label {
                    color: rgba($base-white, .4);

                    span:after {
                        background-color: rgba($base-white, .4);
                    }
                }
            }

            @include hover {
                &:not(._disabled) {
                    &:after {
                        background-color: $opacity-white-40;
                    }

                    .label {
                        color: $opacity-white-40;

                        span:after {
                            background-color: $opacity-white-40;
                            transform: scaleX(0) translateZ(0);
                        }
                    }
                }
            }
        }

        /* Types */
        &._menuItem {
            position: relative;
            padding: 2.6rem 0;

            &:after {
                content: "";
                position: absolute;
                bottom: -.1rem;
                left: 0;
                width: 100%;
                height: .2rem;
                transform: scaleX(0) translateZ(0);
                transform-origin: left center;
                transition: transform $default-transition;
                pointer-events: none;
            }

            &._active {
                &:after {
                    transform: scaleX(1) translateZ(0);
                }
            }

            .label {
                .text {
                    &:after {
                        display: none;
                    }
                }
            }
        }

        &._footerItem {
            &:after {
                display: none;
            }

            .label {
                span:after {
                    display: none;
                }
            }

            &._active {
                &._dark {
                    .label {
                        color: $base-white;
                    }
                }

                &._light {
                    .label {
                        color: $base-600;
                    }
                }
            }

            @include hover {
                &:not(._disabled) {
                    &._dark {
                        .label {
                            color: rgba($base-white, .4);
                        }
                    }

                    &._light {
                        .label {
                            color: $base-400;
                        }
                    }
                }
            }

            &._small {
                font-weight: normal;

                &._dark {
                    .label {
                        color: $opacity-white-80;
                    }
                }

                &._light {
                    .label {
                        color: $base-500;
                    }
                }

                &._active {
                    &._dark {
                        .label {
                            color: $opacity-white-80;
                        }
                    }

                    &._light {
                        .label {
                            color: $base-500;
                        }
                    }
                }

                &._disabled {
                    &._dark {
                        .label {
                            color: $opacity-white-40;
                        }
                    }

                    &._light {
                        .label {
                            color: $base-400;
                        }
                    }
                }

                @include hover {
                    &:not(._disabled) {
                        &._dark {
                            .label {
                                color: $opacity-white-40;
                            }
                        }

                        &._light {
                            .label {
                                color: $base-400;
                            }
                        }
                    }
                }
            }
        }

        /* Modificators */
        &._active:not(._alwaysInteracting) {
            pointer-events: none;
        }

        &._disabled {
            cursor: not-allowed;
        }
    }

    .label {
        display: inline-flex;
        transition: color $default-transition;

        .text {
            position: relative;
            line-height: 130%;

            &:after {
                content: "";
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: .1rem;
                transform: scaleX(1) translateZ(0);
                transform-origin: left center;
                transition: transform $default-transition;
                pointer-events: none;
            }
        }

        svg {
            position: relative;
            top: .4rem;
            display: inline-block;
            width: .64rem;
            height: 1.2rem;
            margin-left: 1.2rem;
            vertical-align: center;
        }
    }
</style>
