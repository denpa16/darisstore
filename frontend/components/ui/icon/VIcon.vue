<template>
    <svg-icon
        :name="name"
        :class="[$style.VIcon, classList]"
    />
</template>

<script>

/**
 * Компонент-обертка для удобного использования иконок
 *
 * @version 1.0.1
 * @displayName VIcon
 */
export default {
    name: 'VIcon',

    props: {
        name: {
            type: String,
            required: true,
        },

        size: {
            type: String,
            default: 'medium',
            validator: v => [
                'xsmall',
                'small',
                'medium',
                'custom',
            ].includes(v),
        },
    },

    computed: {
        classList() {
            return {
                [this.$style[`_size_${this.size}`]]: this.size,
            };
        },
    },
};
</script>

<style lang="scss" module>
    .VIcon {
        fill: currentcolor;

        /* Sizes */

        &._size {
            &_xsmall {
                width: 1.6rem;
                height: 1.6rem;
            }

            &_small {
                width: 2rem;
                height: 2rem;
            }

            &_medium {
                width: 2.4rem;
                height: 2.4rem;
            }
        }
    }
</style>
