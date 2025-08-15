<template>
    <div :class="[$style.VTextarea, classList]">
        <p
            v-if="title"
            :class="$style.title"
        >
            {{ title }}
        </p>

        <div :class="$style.inner">
            <textarea
                ref="textarea"
                :class="$style.native"
                :tabindex="0"
                :value="value"
                v-bind="attributes"
                @blur="onBlur"
                @focus="onFocus"
                @input="onInput"
                @click="$emit('click')"
            />
        </div>
    </div>
</template>

<script>

/**
 * Позволяет пользователю ввести данные с помощью клавитуры.<br>
 * Можно использовать вместе с утилитами из validate-utils, для проверки корректности ввода, по заданному параметру.
 *
 * @version 1.0.1
 * @displayName VTextarea
 */
export default {
    name: 'VTextarea',

    props: {
        /**
         * Определяет классы, которые будут модифицировать размер
         */
        size: {
            type: String,
            default: 'medium',
            validator: value => ['medium'].includes(value),
        },

        /**
         * Определяет классы, которые будут модифицировать цвет
         */
        color: {
            type: String,
            default: 'base',
            validator: val => ['base'].includes(val),
        },

        /**
         * Текущее введёное значение
         */
        value: {
            type: String,
            default: '',
        },

        maxLength: {
            type: String,
            default: '500',
        },

        /**
         * Установить тайтл над инпутом
         */
        title: {
            type: String,
            default: null,
        },

        /**
         * Сообщение пользователю, может использоваться для валидации
         */
        msg: {
            type: String,
            default: '',
        },

        /**
         * Модификатор вида с бордером
         */
        error: Boolean,

        /**
         * Это свойство отключает взаимодействие
         */
        disabled: Boolean,
    },

    data() {
        return {
            isFocused: false,
            lastHeight: 80,
        };
    },

    computed: {
        classList() {
            return {
                [this.$style[`_${this.color}`]]: this.size,
                [this.$style[`_${this.size}`]]: this.size,
                [this.$style._active]: this.isFocused,
                [this.$style._disabled]: this.disabled,
                [this.$style._error]: this.error,
            };
        },

        attributes() {
            const attrs = {
                ...this.$attrs,
                type: 'text',
                disabled: this.disabled,
            };

            if (this.title) {
                attrs.ariaLabel = this.title;
            }

            return attrs;
        },
    },

    methods: {
        /**
         * Эмитит новые значения в родительский компонент.
         * Используется для валидации.
         * @returns {String} e.target.value Введёный текст
         * @public
         */
        onInput(e) {
            /**
             * Возвращает новое значение в родительский компонент.
             * Помогает при валидации поля.
             @param {String} value Новое значение
             */
            this.autoGrow();
            this.$emit('input', e.target.value);
        },

        /**
         * Метод, который обрабатывает событие focus на инпуте
         * @public
         */
        onFocus(e) {
            this.isFocused = true;

            /**
             * Передаёт родителю, что компонент находится в focus.
             * В большинстве реализаций - может и не пригодится
             * @event focus
             */
            this.$emit('focus', e);
        },

        /**
         * Метод, который обрабатывает событие blur на инпуте
         * @public
         */
        onBlur(e) {
            this.isFocused = false;

            /**
             * Передаёт родителю, что компонент больше не находится в focus.
             * В большинстве реализаций - может и не пригодится
             * @event blur
             */
            this.$emit('blur', e);
        },

        autoGrow() {
            if (this.error) {
                this.$refs.textarea.style.height = this.lastHeight + 'px';
                return;
            }
            this.$refs.textarea.style.height = '80px';
            this.$refs.textarea.style.height = this.lastHeight = this.$refs.textarea.scrollHeight + 'px';
        },
    },
};
</script>

<style lang="scss" module>
    $grey-color: $base-500;
    $black-color: $base-900;

    .VTextarea {
        position: relative;
        width: 100%;
        user-select: none;

        /* Sizes */
        &._medium {
            .native {
                padding: 1.4rem 1.6rem;

                @include respond-to(mobile) {
                    // Обязательно в px и не меньше 16px, чтобы не был автозума на айфонах
                    font-size: 16px;
                }
            }
        }

        /* Colors */
        &._base {
            .native {
                background-color: $base-150;
                color: $black-color;
            }

            &._active {
                .native {
                    border-color: $base-300;
                }
            }

            @include hover {
                &:not(._error, ._disabled) {
                    .native {
                        border-color: $base-300;
                    }
                }
            }
        }

        &._active {
            .inner:after {
                transform: scaleX(1);
            }
        }

        &._error {
            .native {
                border-color: $error;
            }
        }

        &._disabled {
            pointer-events: none;

            .native {
                border-color: $grey-color;
                color: $grey-color;
                pointer-events: none;
            }
        }
    }

    .title {
        @include text(m14);

        margin-bottom: 1.2rem;
        color: $base-500;
    }

    .native {
        overflow: hidden;
        width: 100%;
        min-height: 9.2rem;
        border-radius: .6rem;
        border: 1px solid transparent;
    }

    .inner {
        position: relative;
        z-index: 2;
    }
</style>
