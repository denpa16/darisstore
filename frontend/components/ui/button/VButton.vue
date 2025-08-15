<template>
    <VButtonBase
        :tag="tag"
        :to="to"
        :href="href"
        :blank="blank"
        :class="[$style.VButton, 'v-button', classList]"
        :disabled="disabled"
        @click="onClick"
    >
        <transition name="fade-fast" mode="out-in">
            <div v-if="loading" key="loading">
                <TheSpinner/>
            </div>
            <div v-else key="body">
                <slot name="preicon">
                    <VIcon
                        v-if="preicon"
                        :class="$style.icon"
                        :name="preicon"
                    />
                </slot>

                <div
                    v-if="$slots.default"
                    :class="[$style.label, 'v-button-label']"
                >
                    <slot></slot>
                </div>

                <slot name="icon">
                    <VIcon
                        v-if="icon"
                        :class="$style.icon"
                        :name="icon"
                    />
                </slot>
            </div>
        </transition>
    </VButtonBase>
</template>

<script>
import VButtonBase from './VButtonBase.vue';
import TheSpinner from '~/components/common/TheSpinner.vue';

export default {
    name: 'VButton',
    components: { TheSpinner, VButtonBase },

    props: {
        tag: {
            type: String,
            default: 'button',
            validator: v => [
                'n-link',
                'a',
                'span',
                'div',
                'button',
                'input',
            ].includes(v),
        },

        size: {
            type: String,
            default: 'large',
            validator: v => [
                'large',
                'medium',
                'small',
                'custom',
            ].includes(v),
        },

        color: {
            type: String,
            default: 'primary',
            validator: v => [
                'primary',
                'secondary',
                'transparent',
            ].includes(v),
        },

        /**
         * Адрес внутренней ссылки для программного роутинга, преобразующая кнопку в <n-link>
         */
        to: {
            type: String,
            default: '',
        },

        /**
         * Адрес внешней ссылки, преобразующая кнопку в <a>
         */
        href: {
            type: String,
            default: '',
        },

        /**
         * Открывает ссылку в новом окне
         */
        blank: Boolean,

        icon: {
            type: String,
            default: '',
        },

        preicon: {
            type: String,
            default: '',
        },

        active: Boolean,
        disabled: Boolean,
        loading: Boolean,
    },

    computed: {
        classList() {
            return [
                {
                    [this.$style[`_color_${this.color}`]]: this.color,
                    [this.$style[`_size_${this.size}`]]: this.size,
                    [this.$style._icon]: this.icon,
                    [this.$style._preicon]: this.preicon,
                    [this.$style._disabled]: this.disabled,
                    [this.$style._loading]: this.loading,
                    [this.$style._active]: this.active,
                },
            ];
        },
    },

    methods: {
        onClick($event) {
            this.$emit('click', $event);
        },
    },
};
</script>

<style lang="scss" module>
    .VButton {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: .8rem;
        border-radius: .8rem;
        border: 1px solid transparent;
        transition: $default-transition;
        cursor: pointer;
        user-select: none;

        .icon,
        .label {
            transition: $default-transition;
        }

        .label {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            white-space: nowrap;
            line-height: unset;
        }

        /* Sizes */

        &._size {
            &_large {
                @include text(m16);

                height: 5.6rem;
                padding: 0 3.2rem;

                .icon {
                    width: 2rem;
                    height: 2rem;
                }
            }

            &_medium {
                @include text(m16);

                height: 4.8rem;
                padding: 0 3.2rem;

                .icon {
                    width: 2rem;
                    height: 2rem;
                }
            }

            &_small {
                @include text(m14);

                height: 4rem;
                padding: 0 3.2rem;

                .icon {
                    width: 1.6rem;
                    height: 1.6rem;
                }
            }
        }

        /* Colors - Transparent */
        &._color {
            &_primary {
                border-color: $primary-500;
                background-color: $primary-500;

                .label,
                .icon {
                    color: $white;
                }

                @include hover {
                    border-color: $primary-700;
                    background-color: $primary-700;
                }

                &:active,
                &._active {
                    border-color: $primary-900;
                    background-color: $primary-900;
                }
            }

            &_secondary {
                border-color: $primary-150;
                background-color: $white;

                .label,
                .icon {
                    color: $primary-500;
                }

                @include hover {
                    border-color: $primary-500;

                    .label,
                    .icon {
                        color: $primary-700;
                    }
                }

                &:active,
                &._active {
                    border-color: $primary-900;

                    .label,
                    .icon {
                        color: $primary-900;
                    }
                }
            }
        }

        /* Modificators */
        &._disabled {
            border-color: $base-150;
            background-color: $base-150;
            pointer-events: none;

            .label,
            .icon {
                color: $base-300;
            }
        }

        &._loading {
            //
        }
    }

    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(360deg);
        }
    }
</style>
