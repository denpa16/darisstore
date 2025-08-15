<template>
    <VButtonBase
        :class="[$style.VIconButton, 'v-icon-button', classList]"
        :disabled="disabled"
        :tag="tag"
        @click="onClick"
    >
        <slot>
            <VIcon
                v-if="icon"
                :class="$style.icon"
                size="custom"
                :name="icon"
            />
        </slot>
    </VButtonBase>
</template>

<script>
import VButtonBase from '~/components/ui/button/VButtonBase.vue';

export default {
    name: 'VIconButton',
    components: { VButtonBase },

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
            default: 'medium',
            validator: v => [
                'large',
                'medium',
                'small',
                'xsmall',
                'custom',
            ].includes(v),
        },

        color: {
            type: String,
            default: 'primary',
            validator: v => [
                'primary',
                'secondary',
                'custom',
            ].includes(v),
        },

        icon: {
            type: String,
            default: '',
        },

        disabled: Boolean,
        active: Boolean,
    },

    computed: {
        classList() {
            return {
                [this.$style[`_size_${this.size}`]]: this.size,
                [this.$style[`_color_${this.color}`]]: this.color,
                [this.$style._disabled]: this.disabled,
                [this.$style._active]: this.active,
            };
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
    .VIconButton {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: .8rem;
        transition: $default-transition;
        cursor: pointer;

        /* --- Sizes --- */
        &._size {
            &_large {
                width: 5.6rem;
                height: 5.6rem;

                .icon {
                    width: 2.4rem;
                    height: 2.4rem;
                }
            }

            &_medium {
                width: 4.8rem;
                height: 4.8rem;

                .icon {
                    width: 2rem;
                    height: 2rem;
                }
            }

            &_small {
                width: 4rem;
                height: 4rem;

                .icon {
                    width: 1.6rem;
                    height: 1.6rem;
                }
            }

            &_xsmall {
                width: 3.2rem;
                height: 3.2rem;

                .icon {
                    width: 1.6rem;
                    height: 1.6rem;
                }
            }
        }

        /* --- Colors --- */
        &._color {
            &_primary {
                background-color: $primary-500;
                color: $white;

                @include hover {
                    &:not(._disabled) {
                        background-color: $primary-700;
                    }
                }

                &:active,
                &._active {
                    background-color: $primary-900;
                }
            }

            &_secondary {
                background-color: $white;
                color: $primary-300;

                @include hover {
                    &:not(._disabled) {
                        color: $primary-700;
                    }
                }

                &:active,
                &._active {
                    color: $primary-700;
                }
            }
        }

        &._disabled {
            background-color: $base-150;
            color: $base-300;
            cursor: not-allowed;
        }
    }
</style>
