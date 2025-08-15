<template>
    <div :class="[$style.VAccordionItem, classList]" >
        <div
            :class="$style.header"
            @click="toggle(!isOpen)"
        >
            <slot
                name="header-content"
                :open="isOpen"
            >
            </slot>

            <transition name="fade-fast" mode="out-in">
                <VIconButton
                    :key="`btn_${$deviceIs.mobile}`"
                    :class="$style.btn"
                    :size="$deviceIs.mobile ? 'xsmall' : 'small'"
                    color="secondary"
                >
                    <VIcon
                        :class="$style.icon"
                        name="arrow-down"
                        size="xsmall"
                    />
                </VIconButton>
            </transition>
        </div>

        <div
            ref="content"
            :class="$style.contentWrap"
        >
            <div :class="$style.content">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
import { gsap } from 'gsap';

export default {
    name: 'VAccordionItem',

    props: {
        defaultOpened: {
            type: Boolean,
            default: false,
        },
    },

    data() {
        return {
            isOpen: false,
        };
    },

    computed: {
        classList() {
            return [{
                [this.$style._expanded]: this.isOpen,
                [this.$style[`_${this.$parent.color}`]]: this.$parent.color,
            }];
        },
    },

    watch: {
        isOpenOut(val) {
            this.toggle(val);
        },
    },

    beforeMount() {
        this.$parent.register(this);
    },

    mounted() {
        if (this.defaultOpened) {
            this.toggle(this.defaultOpened);
        }
    },

    beforeDestroy() {
        this.$parent.unregister(this);
    },

    methods: {
        toggle(value) {
            if (value !== this.isOpen) {
                this.isOpen = value;
                this.$parent.setOpen(this, this.isOpen);
            }

            this.animate();
        },

        animate() {
            if (!this.$refs.content) {
                return;
            }

            if (this.isOpen) {
                gsap.to(this.$refs.content, {
                    duration: .4,
                    height: 'auto',
                });
            } else {
                gsap.to(this.$refs.content, {
                    duration: .4,
                    height: 0,
                });
            }
        },
    },
};
</script>

<style lang="scss" module>
    .VAccordionItem {
        position: relative;
        padding: 2rem;
        border-radius: 1.2rem;
        background-color: $base-150;
        transition: background-color $default-transition, color $default-transition;

        &._expanded {
            & .icon {
                transform: rotateZ(-180deg);
            }
        }
    }

    .header {
        @include text(s16);

        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.6rem;
        color: $base-700;
        cursor: pointer;
        user-select: none;
    }

    .contentWrap {
        overflow: hidden;
        height: 0;
    }

    .content {
        @include text(r16);

        margin-top: 1.6rem;
        margin-right: 4rem;
        color: $base-500;

        @include respond-to(mobile) {
            @include text(r14);

            margin-right: 0;
        }
    }

    .btn {
        flex-shrink: 0;
    }

    .icon {
        color: $primary-300;
        transition: transform $default-transition;
    }
</style>
