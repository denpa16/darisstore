<template>
    <div
        ref="activator"
        class="VTooltip"
        @mouseenter="onActivatorEnter"
        @mouseleave="onActivatorLeave"
        @click="onActivatorClick"
    >

        <slot name="activator"></slot>

        <div
            ref="content"
            :class="['c-tooltip__content', {'is-hoverable': hoverable}]"
            :style="position"
            @mouseenter="onContentEnter"
            @mouseleave="onContentLeave"
        >
            <transition name="tooltip">
                <div v-if="isVisible">
                    <slot></slot>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VTooltip',

    props: {
        /**
         * Селектор элемента в который будет вставлен тултип.
         * Должен иметь свойство position: relative или  position: absolute
         */
        attach: {
            type: String,
            default: '#app',
        },

        top: Boolean,
        bottom: Boolean,
        left: Boolean,
        right: Boolean,
        hoverable: Boolean,

        /**
         * Отступ от активатора до тултипа
         */
        nudge: {
            type: Number,
            default: 8,
        },

        /**
         * Вертикальный отступ от краев экрана до тултипа
         */
        offsetY: {
            type: Number,
            default: 12,
        },

        /**
         * Горизонтальный отступ от краев экрана до тултипа
         */
        offsetX: {
            type: Number,
            default: 12,
        },
    },

    data() {
        return {
            dimensions: {
                activator: {
                    top: 0,
                    left: 0,
                    width: 0,
                    height: 0,
                },

                content: {
                    top: 0,
                    left: 0,
                    width: 0,
                    height: 0,
                },

                page: {
                    top: 0,
                    left: 0,
                    width: 0,
                    height: 0,
                },

                attach: {
                    top: 0,
                    left: 0,
                    width: 0,
                    height: 0,
                },
            },

            isVisible: false,
            isDetached: false,
            target: null,
            timeout: null,
            clickTimeout: null,
        };
    },

    computed: {
        position() {
            const { activator, content } = this.dimensions;
            const unknown = !this.bottom && !this.left && !this.top && !this.right;

            let top = 0;
            let left = 0;

            if (this.top || this.bottom || unknown) {
                top =
                    activator.top +
                    (this.bottom ? activator.height : -content.height) +
                    (this.bottom ? this.nudge : -this.nudge);

                left = activator.left + activator.width / 2 - content.width / 2;
            } else if (this.left || this.right) {
                top = activator.top + activator.height / 2 - content.height / 2;

                left =
                    activator.left +
                    (this.right ? activator.width : -content.width) +
                    (this.right ? this.nudge : -this.nudge);
            }

            top = this.calcYOverflow(top);
            left = this.calcXOverflow(left);

            return {
                top: `${this.attach ? top - this.dimensions.attach.top : top}px`,
                left: `${this.attach ? left - this.dimensions.attach.left : left}px`,
            };
        },
    },

    mounted() {
        if (!this.$slots.activator) {
            console.error('[VTooltip] activator slot must be bound');
        }
    },

    beforeDestroy() {
        if (this.isDetached && this.target) {
            this.target.removeChild(this.$refs.content);
        }
    },

    methods: {
        handleInit() {
            if (!this.isDetached) {
                this.initDetach();
            }

            if (this.timeout && this.isVisible) {
                clearTimeout(this.timeout);
                this.timeout = null;
            } else {
                this.$emit('enter');
                this.isVisible = true;
                this.$nextTick(() => {
                    this.updateDimensions();
                });
            }
        },

        onActivatorEnter() {
            if (this.$deviceIs.mobile) {
                return;
            }

            this.handleInit();
        },

        onActivatorClick() {
            if (this.$deviceIs.mobile) {
                if (this.isVisible) {
                    this.onActivatorLeave();
                    return;
                }

                this.handleInit();

                this.clickTimeout = setTimeout(() => {
                    this.onActivatorLeave();
                }, 5000);
            }
        },

        onActivatorLeave() {
            this.hide();
        },

        onContentEnter() {
            if (!this.hoverable) {
                return;
            }

            clearTimeout(this.timeout);
            this.timeout = null;
        },

        onContentLeave() {
            if (!this.hoverable) {
                return;
            }
            this.hide();
        },

        hide() {
            this.timeout = setTimeout(() => {
                this.isVisible = false;
                clearTimeout(this.timeout);
                clearTimeout(this.clickTimeout);
                this.timeout = null;
                this.clickTimeout = null;
                this.$emit('blur');
            }, 50);
        },

        updateDimensions() {
            if (this.$refs.activator) {
                const activatorBounding = this.$refs.activator.getBoundingClientRect();
                this.dimensions.activator.top = activatorBounding.top + window.pageYOffset;
                this.dimensions.activator.left = activatorBounding.left + window.pageXOffset;
                this.dimensions.activator.width = activatorBounding.width;
                this.dimensions.activator.height = activatorBounding.height;
            } else {
                console.warn('[CTooltip] updateDimensions error - activator is undefined');
            }

            if (this.$refs.content) {
                const contentBounding = this.$refs.content.getBoundingClientRect();
                this.dimensions.content.top = contentBounding.top + window.pageYOffset;
                this.dimensions.content.left = contentBounding.left + window.pageXOffset;
                this.dimensions.content.width = contentBounding.width;
                this.dimensions.content.height = contentBounding.height;
            } else {
                console.warn('[CTooltip] updateDimensions error - content is undefined');
            }

            this.dimensions.page.width = document.documentElement.clientWidth || window.innerWidth;
            this.dimensions.page.height =
                document.documentElement.clientHeight || window.innerHeight;
            this.dimensions.page.top = window.pageYOffset || document.documentElement.scrollTop;
            this.dimensions.page.left = window.pageXOffset || document.documentElement.scrollLeft;

            if (this.attach) {
                const attachEl = document.querySelector(this.attach);
                if (attachEl) {
                    const attachBounding = attachEl.getBoundingClientRect();
                    this.dimensions.attach.top = attachBounding.top + window.pageYOffset;
                    this.dimensions.attach.left = attachBounding.left + window.pageXOffset;
                    this.dimensions.attach.width = attachBounding.width;
                    this.dimensions.attach.height = attachBounding.height;
                }
            }
        },

        calcYOverflow(top) {
            /**
             * @param {top} - верхняя граница тултипа
             */
            const topOverflow = this.dimensions.page.top + this.offsetY - top;
            const bottomOverflow =
                top +
                this.dimensions.content.height +
                this.offsetY -
                (this.dimensions.page.top + this.dimensions.page.height);

            let attachTopOverflow = 0;
            let attachBottomOverflow = 0;

            if (this.attach) {
                attachTopOverflow = this.dimensions.attach.top + this.offsetY - top;
                attachBottomOverflow =
                    top +
                    this.dimensions.content.height +
                    this.offsetY -
                    (this.dimensions.attach.top + this.dimensions.attach.height);
            }

            if (topOverflow > 0) {
                top = this.dimensions.page.top + this.offsetY;
            } else if (this.attach && attachTopOverflow > 0) {
                top = this.dimensions.attach.top + this.offsetY;
            } else if (bottomOverflow > 0) {
                top =
                    this.dimensions.page.top +
                    this.dimensions.page.height -
                    this.offsetY -
                    this.dimensions.content.height;
            } else if (this.attach && attachBottomOverflow > 0) {
                top =
                    this.dimensions.attach.top +
                    this.dimensions.attach.height -
                    this.offsetY -
                    this.dimensions.content.height;
            }

            return top;
        },

        calcXOverflow(left) {
            const leftOverflow = this.dimensions.page.left + this.offsetX - left;
            const rightOverflow =
                left +
                this.dimensions.content.width +
                this.offsetX -
                (this.dimensions.page.left + this.dimensions.page.width);

            let attachLeftOverflow = 0;
            let attachRightOverflow = 0;

            if (this.attach) {
                attachLeftOverflow =
                    this.dimensions.attach.left + this.offsetY - left;
                attachRightOverflow =
                    left +
                    this.dimensions.content.width +
                    this.offsetY -
                    (this.dimensions.attach.left + this.dimensions.attach.width);
            }

            if (this.attach && attachLeftOverflow > 0) {
                left = this.dimensions.attach.left + this.offsetY;
            } else if (leftOverflow > 0) {
                left = this.dimensions.page.left + this.offsetX;
            } else if (this.attach && attachRightOverflow > 0) {
                left =
                    this.dimensions.attach.left +
                    this.dimensions.attach.width -
                    this.offsetY -
                    this.dimensions.content.width;
            } else if (rightOverflow > 0) {
                left =
                    this.dimensions.page.left +
                    this.dimensions.page.width -
                    this.offsetX -
                    this.dimensions.content.width;
            }

            return left;
        },

        initDetach() {
            this.target = document.querySelector(this.attach);

            if (!this.target) {
                console.warn(`[CTooltip] Unable to locate target ${this.attach}`);
                return;
            }

            try {
                this.target.appendChild(this.$refs.content);
            } catch (e) {
                console.log(e);
            }

            this.isDetached = true;
        },
    },
};
</script>

<style lang="scss">
    .c-tooltip {
        cursor: pointer;

        &__content {
            position: absolute;
            z-index: 2000;
            pointer-events: none;

            &.is-hoverable {
                pointer-events: all;
            }

            & > div {
                @include text(r14);

                padding: .8rem;
                border-radius: .4rem;
                background: $base-700;
                color: $white;
            }
        }
    }

    .tooltip-enter-active {
        transition: opacity .3s, transform .3s;
    }

    .tooltip-leave-active {
        transition: opacity .15s, transform .15s;
    }

    .tooltip-enter,
    .tooltip-leave-active {
        opacity: 0;
        transform: translateY(-1.6rem);
    }
</style>
