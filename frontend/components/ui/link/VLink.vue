<template>
    <component
        :is="component"
        :class="$style.VLink"
        v-bind="attrs"
        @click="$emit('click')"
    >
        <slot></slot>
    </component>
</template>

<script>

/**
 * Компонент динамической ссылки. В зависимости от передаваемых данных
 * преобразуется либо в обычную внешнюю ссылку, либо в линк для программного роутинга.
 * Удобно использовать в списках, где могут быть оба вида ссылок.
 *
 */

export default {
    name: 'VLink',

    props: {
        link: {
            type: String,
            default: '',
        },

        href: {
            type: String,
            default: '',
        },

        blank: {
            type: Boolean,
            default: false,
        },

        defaultInline: {
            type: Boolean,
            default: false,
        },

        isPhone: {
            type: Boolean,
            default: false,
        },

        isEmail: {
            type: Boolean,
            default: false,
        },
    },

    computed: {
        component() {
            if (this.link) {
                return 'n-link';
            }

            if (this.href) {
                return 'a';
            }

            return this.defaultInline ? 'span' : 'div';
        },

        attrs() {
            const res = {};

            if (this.link) {
                res.to = this.link;
            }

            if (this.href) {
                if (this.isPhone) {
                    res.href = `tel:${this.href}`;
                } else if (this.isEmail) {
                    res.href = `mailto:${this.href}`;
                } else {
                    res.href = this.href;
                }

                res.rel = 'nofollow noopener';
            }

            if (this.blank || this.href) {
                res.target = '_blank';
            }

            return res;
        },
    },
};
</script>

<style lang="scss" module>
    .VLink {
        //
    }
</style>
