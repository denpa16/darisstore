<template>
    <transition
        duration="500"
        mode="out-in"
        name="modal"
        @before-enter="beforeEnter"
        @after-leave="afterLeave"
    >
        <div
            v-if="component"
            :key="key"
            :class="[$style.TheModal, classList]"
        >
            <div :class="$style.wrapper">
                <div
                    v-clickoutside="close"
                    :class="$style.container"
                    data-scroll-lock-scrollable
                >
                    <component
                        :is="component"
                        :key="key"
                        v-bind="attrs"
                        @change="onChange"
                        @close="close"
                    />
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
// Utils
import { disablePageScroll, enablePageScroll } from 'scroll-lock/dist/scroll-lock';
import { mapGetters } from 'vuex';

export default {
    name: 'TheModal',

    data() {
        return {
            component: null,
            attrs: null,
            size: null,
            onClose: null,
            key: null,
            isPopover: false,
            isShowHeader: false,
        };
    },

    computed: {
        ...mapGetters({
            hasPromo: 'menu/getHasPromo',
        }),

        classList() {
            return {
                [this.$style[`_${this.attrs?.position}`]]: this.attrs?.position,
                [this.$style[`_size_${this.size || 'medium'}`]]: true,
                [this.$style._showHeader]: this.isShowHeader,
                [this.$style._hasPromo]: this.hasPromo,
                [this.$style._popover]: this.isPopover,
            };
        },
    },

    beforeMount() {
        this.$modal.event.$on('open', this.open);
        this.$modal.event.$on('update', this.update);
        this.$modal.event.$on('close', this.close);
    },

    beforeDestroy() {
        this.$modal.event.$off('open', this.open);
        this.$modal.event.$off('update', this.update);
        this.$modal.event.$off('close', this.close);
        enablePageScroll();
        this.isPopover = false;
    },

    methods: {
        onChange(val) {
            this.$modal.event.$emit('change', val);
            if (val === 'reset') {
                this.close();
            }
        },

        open(component, attrs, onClose) {
            this.component = component;
            this.attrs = attrs;
            this.size = this.attrs?.size;
            this.isPopover = this.attrs?.isPopover;
            this.isShowHeader = this.attrs?.isShowHeader;
            this.onClose = onClose;
            this.key = Math.random();
        },

        update(attrs) {
            this.attrs = attrs;
        },

        close() {
            if (this.onClose) {
                this.onClose();
            }

            this.$modal.event.$off('change');
            this.component = this.attrs = this.onClose = this.key = null;
        },

        beforeEnter() {
            disablePageScroll();
        },

        afterLeave() {
            enablePageScroll();
            this.isPopover = false;
        },
    },
};
</script>

<style lang="scss" module>
    .TheModal {
        &._popover {
            z-index: calc(#{$header-z-index} - 10);

            &._left .wrapper {
                left: 0;
            }

            &._right .wrapper {
                right: 0;
            }

            .wrapper {
                position: absolute;
                width: 30rem;

                @include respond-to(mobile) {
                    width: 100vw;
                }
            }

            .container {
                position: absolute;
                bottom: 0;
                overflow: hidden;
                width: 100%;
            }
        }

        &._showHeader {
            top: $header-h;

            @include respond-to(tablet) {
                top: $header-h-mobile;

                &._hasPromo {
                    top: calc($header-h-mobile + $promo-h-tablet);
                }
            }
        }

        &._left {
            &:global(.modal-enter),
            &:global(.modal-leave-active) {
                .container {
                    transform: translate3d(-100%, 0, 0);
                }
            }
        }

        &._right {
            &:global(.modal-enter),
            &:global(.modal-leave-active) {
                .container {
                    transform: translate3d(100%, 0, 0);
                }
            }

            .container {
                border-radius: 2rem 0 0 2rem;

                @include respond-to(mobile) {
                    border-radius: 0;
                }
            }
        }

        &._size {
            &_medium {
                .container {
                    width: 51.6rem;

                    @include respond-to(tablet) {
                        width: 50vw;
                    }

                    @include respond-to(mobile) {
                        width: 100%;
                    }
                }
            }

            &_large {
                .container {
                    width: 73rem;

                    @include respond-to(tablet) {
                        width: 60rem;
                    }

                    @include respond-to(mobile) {
                        width: 100%;
                    }
                }
            }
        }

        &:global(.modal-enter-active),
        &:global(.modal-leave-to) {
            &:after {
                opacity: 1;
                transition: opacity .3s ease;
            }

            .container {
                opacity: 1;
                transform: translate3d(0, 0, 0);
                transition: opacity .2s ease .3s, transform .2s ease .3s;
            }
        }

        &:global(.modal-enter),
        &:global(.modal-leave-active) {
            &:after {
                opacity: 0;
                transition: opacity .3s ease .2s;
            }

            .container {
                opacity: 0;
                transform: translate3d(100%, 0, 0);
                transition: opacity .2s ease, transform .2s ease;

                @include respond-to(tablet) {
                    transform: translate3d(0, 100%, 0);
                }
            }
        }

        &:after {
            content: "";
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            z-index: 1;
            background-color: rgba($base-700, .4);
        }

        .wrapper {
            position: relative;
            z-index: 2;
            display: flex;
            align-items: flex-start;
            justify-content: flex-end;
            width: 100%;
            height: 100%;
        }

        .container {
            overflow-y: auto;
            display: block;
            width: 51.6rem;
            height: 100%;
            background-color: #fff;

            @include respond-to(tablet) {
                width: 44rem;
            }

            @include respond-to(mobile) {
                position: absolute;
                bottom: 0;
                width: 100%;
            }
        }
    }
</style>
