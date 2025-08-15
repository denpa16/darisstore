<template>
    <div :class="[$style.VInput, classList]">
        <div v-if="title" :class="$style.titleWrap">
            <p
                :class="$style.title"
            >
                {{ title }}
            </p>
        </div>

        <div :class="$style.inner">
            <input
                :class="$style.native"
                :tabindex="0"
                :value="inputValue"
                v-bind="attributes"
                @blur="onBlur"
                @focus="onFocus"
                @input="onInput"
                @click="$emit('click')"
            >

            <VTooltip v-if="msg" :class="$style.tooltip">
                <template #activator>
                    <VIcon
                        size="custom"
                        name="information"
                        :class="$style.information"
                    />
                </template>

                <template #default>
                    {{ msg }}
                </template>
            </VTooltip>

            <div
                v-if="premask"
                :class="$style.premask"
                v-html="currentPremask"
            >
            </div>
        </div>
    </div>
</template>

<script>
// Utils
import { masks, numberInputs, addMask, setCursor } from '~/assets/js/utils/mask-utils';

/**
 * Позволяет пользователю ввести данные с помощью клавитуры.<br>
 * Можно использовать вместе с утилитами из validate-utils, для проверки корректности ввода, по заданному параметру.
 *
 * @version 1.0.1
 * @displayName VInput
 */
export default {
    name: 'VInput',

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
         * Тип, для передачи в атрибуты нативного инпута
         */
        type: {
            type: String,
            default: 'text',
        },

        /**
         * Текущее введёное значение
         */
        value: {
            type: String,
            default: '',
        },

        /**
         * Даёт возможность отключить autocomplete при вводе
         */
        autocomplete: {
            type: Boolean,
            default: true,
        },

        /**
         * Позволяет отображать лейбл после ввода
         */
        keepLabel: {
            type: Boolean,
            default: false,
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
         * Параметр маски инпута, если необходим
         * @values phone, date, time, number, snils, inn, passport, payment, percent, year, pin, months
         */
        mask: {
            type: String,
            default: '',
        },

        /**
         * Отображение маску при вводе
         */
        premask: {
            type: Boolean,
            default: true,
        },

        /**
         * Если активно, то при эмите, данные будут переданы с учётом активной маски.
         * Т.е. если в инпуте компонента +7 (999) 00-00-00, то без этого параметра,
         * будет передано 9990000. Включено по-умолчанию, для валидации
         */
        keepMasked: {
            type: Boolean,
            default: true,
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
            currentMask: '',
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

        inputValue() {
            if (this.mask) {
                return addMask(this.value, this.currentMask);
            }
            return this.value;
        },

        currentPremask() {
            if (!this.mask) {
                return '';
            }

            if (this.inputValue.length) {
                const regex = new RegExp('^.{0,' + this.inputValue.length + '}', 'g');
                const pre = this.currentMask.replace(regex, `<span>${this.inputValue}</span>`);
                return pre.replace(/#/g, '&ensp;');
            } else {
                return this.currentMask.replace(/#/g, '&ensp;');
            }
        },

        attributes() {
            const attrs = {
                ...this.$attrs,
                type: 'text',
                disabled: this.disabled,
            };

            if (this.mask) {
                attrs.maxlength = this.currentMask.length;
            }

            if (this.maxLength) {
                attrs.maxlength = this.maxLength;
            }

            if (this.type) {
                if (this.mask) {
                    attrs.type = numberInputs.includes(this.mask) ? 'tel' : 'text';
                } else {
                    attrs.type = this.type;
                }
            }

            if (!this.autocomplete) {
                attrs.autocomplete = 'off';
            }

            return attrs;
        },

        hintColor() {
            if (this.disabled) {
                return 'lightGrey';
            }

            return this.error ? 'error' : this.color;
        },
    },

    created() {
        if (this.mask) {
            try {
                this.currentMask = masks[this.mask];
                if (!this.currentMask) {
                    throw new Error(`VInput: mask-utils: mask ${this.mask} not found`);
                }
            } catch (e) {
                console.log(e);
            }
        }
    },

    methods: {
        /**
         * Эмитит новые значения в родительский компонент.
         * Используется для валидации.
         * @returns {String} e.target.value Введёный текст
         * @public
         */
        onInput(e) {
            if (this.mask) {
                let position = e.target.selectionEnd;
                const digit = e.target.value[position - 1];

                if (this.mask === 'phone') {
                    // Заменяет скобки и тире при вводе копированием
                    if (e.target.value.matchAll(/\(|\)|-/ig)) {
                        e.target.value = e.target.value.replace(/\(|\)|-/ig, '');
                    }

                    // Заменяет 8 при вводе на +7,
                    // если это первый символ
                    if (e.target.value.charAt(0) == 8) {
                        e.target.value = '+7';
                    }
                }

                e.target.value = addMask(e.target.value, this.currentMask);

                if (position !== 0) {
                    while (position < e.target.value.length && e.target.value.charAt(position - 1) !== digit) {
                        position++;
                    }
                }

                setCursor(e.target, position);

                if (this.mask === 'percent') {
                    if (e.target.value === '00') {
                        e.target.value = 1;
                    }
                    e.target.value = e.target.value > 100 ? '100%' : e.target.value + '%';
                } else if (this.mask === 'months') {
                    if (e.target.value > 360) {
                        e.target.value = 360;
                    }
                }
                if (e.target.value !== this.inputValue) {
                    const emitVal = this.keepMasked
                        ? e.target.value
                        : addMask(e.target.value, this.currentMask, false);
                    this.$emit('input', emitVal);
                    return;
                }
            }

            /**
             * Возвращает новое значение в родительский компонент.
             * Помогает при валидации поля.
             @param {String} value Новое значение
             */
            this.$emit('input', e.target.value);
        },

        /**
         * Метод, который обрабатывает событие focus на инпуте
         * @public
         */
        onFocus(e) {
            this.isFocused = true;

            // Automatically add '+7' characters
            if (this.mask && this.mask === 'phone' && !this.inputValue) {
                this.$nextTick(() => {
                    setCursor(e.target, this.inputValue.length);
                });
            }

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

            // Automatically remove '+' or '+7' character
            if (this.mask && this.mask === 'phone' && (this.inputValue === '+' || this.inputValue === '+7')) {
                this.$emit('input', '');
            }
        },
    },
};
</script>

<style lang="scss" module>
    $grey-color: $base-500;
    $black-color: $base-900;

    .VInput {
        position: relative;
        width: 100%;
        user-select: none;

        /* Sizes */
        &._medium {
            .native {
                padding: 1.4rem 1.6rem;
            }

            .premask,
            .native {
                @include respond-to(mobile) {
                    // Обязательно в px и не меньше 16px, чтобы не был автозума на айфонах
                    font-size: 16px;
                }
            }
        }

        /* Colors */
        &._base {
            .native {
                border-radius: .6rem;
                border: 1px solid transparent;
                background-color: $base-150;
                color: $black-color;
                transition: $default-transition;
            }

            .premask {
                color: $grey-color;
            }

            &._active {
                .native {
                    border-color: $base-300;
                }
            }

            @include hover {
                .native {
                    border-color: $base-300;
                }
            }
        }

        /* Mods */
        &._active {
            .inner:after {
                transform: scaleX(1);
            }
        }

        &._error {
            input.native {
                border-color: $error;
            }

            @include hover {
                input.native {
                    border-color: $error;
                }
            }
        }

        &._disabled {
            pointer-events: none;

            .native {
                border-color: $grey-color;
                color: $grey-color;
                pointer-events: none;
            }

            .icon,
            .description {
                color: $base-300;
                fill: $base-300;
            }
        }
    }

    .titleWrap {
        display: flex;
        align-items: flex-start;
    }

    .title {
        @include text(m14);

        margin-bottom: 1.2rem;
        color: $base-500;
    }

    .premask,
    .native {
        width: 100%;
    }

    .inner {
        position: relative;
        z-index: 2;
    }

    .premask {
        position: absolute;
        top: 50%;
        left: 2rem;
        z-index: 1;
        display: inline-flex;
        height: min-content;
        margin: 0;
        opacity: 0;
        transform: translateY(-50%);
        transition: opacity $default-transition;
        user-select: none;
        pointer-events: none;

        @include respond-to(mobile) {
            bottom: -.3rem;
        }
    }

    .icon {
        width: 1.4rem;
        min-width: 1.4rem;
        height: 1.4rem;
        min-height: 1.4rem;
        pointer-events: all;
        transition: color .2s;
        cursor: pointer;
        user-select: none;

        @include hover {
            color: $black-color;
        }
    }

    .tooltip {
        position: absolute;
        top: 50%;
        right: 1.6rem;
        width: 2rem;
        height: 2rem;
        transform: translateY(-50%);
    }

    .information {
        width: 2rem;
        height: 2rem;
        color: $error;
    }
</style>
