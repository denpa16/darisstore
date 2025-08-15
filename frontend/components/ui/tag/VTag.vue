<template>
    <component
        :is="tag"
        :class="[$style.VTag, classes]"
        @click="$emit('click', $event)"
    >
        <slot>
            <span v-html="label"></span>
        </slot>
    </component>
</template>

<script>
export default {
    name: 'VTag',

    props: {
        tag: {
            type: String,
            default: 'div',
        },

        /**
         * Определяет классы, которые будут модифицировать размер
         */
        size: {
            type: String,
            default: 'medium',
            validator: v => [
                'medium',
                'custom',
            ].includes(v),
        },

        /**
         * Определяет классы, которые будут модифицировать цвет
         */
        color: {
            type: String,
            default: 'white',
            validator: v => [
                'white',
                'light',
                'custom',
            ].includes(v),
        },

        label: {
            type: String,
            default: '',
        },
    },

    computed: {
        classes() {
            return {
                [this.$style[`_size_${this.size}`]]: this.size,
                [this.$style[`_color_${this.color}`]]: this.color,
            };
        },
    },
};
</script>

<style lang="scss" module>
    .VTag {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: $radius-max;
        white-space: nowrap;
        transition: background-color $default-transition, color $default-transition;
        user-select: none;

        /* Sizes */

        &._size {
            &_medium {
                @include text(m12);

                padding: .9rem 1.2rem;
            }
        }

        /* End sizes */

        /* Colors */

        &._color {
            &_white {
                background-color: $white;
                color: $base-900;
            }

            &_light {
                background-color: $base-150;
                color: $base-900;
            }
        }
    }
</style>
