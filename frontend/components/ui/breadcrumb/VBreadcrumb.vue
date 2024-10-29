<script setup
        lang="ts"
>
// #region Imports
import type { TColor, TSize, TTheme } from '@/types/ui/type.ts';
// #endregion

// #region Props
export interface Breadcrumb {
    title: string;
    link: string;
    disabled?: boolean;
}

interface IProps {
    size?: Extract<TSize, 'small' | 'medium'>,
    theme?: TTheme,
    color?: Extract<TColor, 'primary'>,
    breadcrumbs: Array<Breadcrumb>,
    separator?: 'slash' | 'point',
    name?: '',
}

const props = withDefaults(defineProps<IProps>(), {
    size: 'medium',
    theme: 'light',
    color: 'primary',
    separator: 'slash',
    name: '',
});
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${props.theme}`]]: props.color,
        [$style[`_${props.color}`]]: props.color,
        [$style[`_${props.size}`]]: props.size,
        [$style[`_${props.separator}`]]: props.separator,
    },
]);
// #endregion

</script>

<template>
    <ul
        :class="[$style.VBreadcrumb, classList]"
        :data-test-id="name"
    >
        <li
            v-for="(breadcrumb, index) in breadcrumbs"
            :key="index"
            :class="[$style.item, {
                [$style._disabled]: breadcrumb.disabled,
            }]"
        >
            <NuxtLink
                :class="$style.link"
                :to="breadcrumb.link"
            >
                {{ breadcrumb.title }}
            </NuxtLink>
        </li>
    </ul>
</template>

<style lang="scss"
       module
>
    $base: $primary-100;
    $base-hover: $primary-hover;
    $base-disable: $base-400;

    .VBreadcrumb {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        padding: 3.2rem 0 1.2rem;
        list-style: none;

        /* Sizes */
        &._small {
            .item {
                font-size: 1.4rem;

                &:not(:last-child) {
                    margin-right: 1.8rem;

                    &:after {
                        right: -1rem;
                        width: .3rem;
                        height: .3rem;
                    }
                }
            }
        }

        &._medium {
            .item {
                font-size: 1.6rem;

                &:not(:last-child) {
                    margin-right: 2.2rem;

                    &:after {
                        right: -1.3rem;
                        width: .4rem;
                        height: .4rem;
                    }
                }
            }
        }

        /* Themes */
        &._light {
            &._primary {
                .item {
                    color: $base;

                    &._disabled {
                        color: $base-disable;

                        .link {
                            color: $base-disable;
                        }
                    }

                    &:not(:last-child) {
                        &:after {
                            background-color: $base-disable;
                            color: $base-disable;
                        }
                    }
                }

                .link {
                    color: $base;

                    @include hover {
                        &:hover {
                            color: $base-hover;
                        }
                    }
                }
            }
        }

        &._dark {
            &._primary {
                .item {
                    color: $base-disable;

                    &._disabled {
                        color: $base;

                        .link {
                            color: $base;
                        }
                    }

                    &:not(:last-child) {
                        &:after {
                            background-color: $base;
                            color: $base;
                        }
                    }
                }

                .link {
                    color: $base-disable;

                    @include hover {
                        &:hover {
                            color: $base-hover;
                        }
                    }
                }
            }
        }

        /* Modifiers */
        &._point {
            .item:not(:last-child):after {
                content: "";
            }
        }

        &._slash {
            .item:not(:last-child):after {
                content: "/";
                right: -.8rem;
                width: 0;
                height: 100%;
                color: $base-disable;
            }
        }
    }

    .item {
        position: relative;
        display: flex;
        align-items: center;
        line-height: 1;
        letter-spacing: -.005em;
        user-select: none;

        &._disabled {
            pointer-events: none;
        }

        &:not(:last-child) {
            &:after {
                position: absolute;
                border-radius: 50%;
                transition: color $default-transition, background-color $default-transition;
            }
        }
    }

    .link {
        color: $base;
        transition: color $default-transition;
        cursor: pointer;
    }
</style>
