<template>
    <div :class="$style.VAccordion">
        <!-- @slot Список компонентов VAccordionItem -->
        <slot></slot>
    </div>
</template>

<script>

/**
 * Позволяет пользователям отображать и скрывать разделы связанного контента на странице.
 *
 * @version 1.0.1
 * @displayName VAccordion
 */

export default {
    name: 'VAccordion',

    props: {
        /**
         * Определяет возможность раскрывать несколько элементов одновременно
         */
        multiple: {
            type: Boolean,
            default: false,
        },

        /**
         * Определяет классы, которые будут модифицировать цвет
         */
        color: {
            type: String,
            default: 'base',
            validator: val => ['base', 'dark', 'secondary', 'inherit', 'milk'].includes(val),
        },

        /**
         * Определяет классы, которые будут модифицировать размер
         */
        size: {
            type: String,
            default: 'default',
            validator: val => ['default', 'custom'].includes(val),
        },

        /**
         * Определяет наличие тени
         */
        shadow: {
            type: Boolean,
            default: false,
        },
    },

    data() {
        return {
            panels: [],
            open: null,
        };
    },

    methods: {
        register(panel) {
            this.panels.push(panel);
        },

        unregister(panel) {
            if (!this.multiple && this.open === panel) {
                this.open = null;
            }

            const index = this.panels.findIndex(p => p._uid === panel._uid);
            this.panels.splice(index, 1);
        },

        setOpen(panel, isOpen) {
            if (!this.multiple) {
                for (let i = 0; i < this.panels.length; i++) {
                    const item = this.panels[i];
                    if (isOpen === true && item._uid !== panel._uid) {
                        item.toggle(false);
                    }
                }

                if (isOpen === false) {
                    this.open = null;
                } else {
                    this.open = panel;
                }
            }
        },
    },
};
</script>

<style lang="scss" module>
    .VAccordion {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        gap: 1.6rem;
    }
</style>
