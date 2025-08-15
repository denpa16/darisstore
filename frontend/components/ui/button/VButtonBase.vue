<template>
    <component
        :is="component"
        :disabled="disabled"
        v-bind="attrs"
        @click="onClick"
    >
        <slot></slot>
    </component>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'VButtonBase',
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

        /**
         * Адрес внутренней ссылки для программного роутинга, преобразующая кнопку в <n-link>
         */
        link: {
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

        disabled: Boolean,
    },

    computed: {
        component() {
            if (this.tag !== 'button') {
                return this.tag;
            }

            if (this.href) {
                return 'a';
            }

            if (this.to) {
                return 'n-link';
            }

            return 'button';
        },

        attrs() {
            switch (this.component) {
                case this.tag:
                    return this.$attrs;

                case 'a':
                    return {
                        ...this.$attrs,
                        href: this.href,
                        target: '_blank',
                        rel: 'nofollow noopener',
                    };

                case 'n-link': {
                    const res = {
                        ...this.$attrs,
                        to: this.to,
                    };

                    if (this.blank) {
                        res.target = '_target';
                    }

                    return res;
                }

                default:
                    return this.$attrs;
            }
        },
    },

    methods: {
        /**
         * Эмитит событие клика в родительский компонент
         * @param {Event} event mouse event
         * @public
         */
        onClick(event) {
            /**
             * Cобытие клика в родительский компонент
             * @event click
             * @param {Event} event mouse event
             */
            if (this.disabled) {
                return;
            }

            this.$emit('click', event);
        },
    },
});
</script>
