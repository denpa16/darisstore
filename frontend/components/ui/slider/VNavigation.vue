<template>
    <div :class="$style.VNavigation">
        <VIconButton
            ref="prev"
            :class="['nav-prev', $style.btn]"
            :color="colorButtons"
            :size="sizeButtons"
            :disabled="disabled || (!loop && current === min)"
            icon="arrow-left"
            @click="$emit('prev')"
        />

        <VIconButton
            ref="next"
            :class="['nav-next', $style.btn]"
            :color="colorButtons"
            :size="sizeButtons"
            :disabled="disabled || (!loop && current === max)"
            icon="arrow-right"
            @click="$emit('next')"
        />
    </div>
</template>

<script>
import VIconButton from '~/components/ui/button/VIconButton.vue';

export default {
    name: 'VNavigation',

    components: {
        VIconButton,
    },

    props: {
        min: {
            type: Number,
            default: 0,
        },

        max: {
            type: Number,
            required: true,
            default: 0,
        },

        index: {
            type: Number,
            required: true,
            default: 0,
        },

        loop: {
            type: Boolean,
            default: false,
        },

        disabled: {
            type: Boolean,
            default: false,
        },

        sizeButtons: {
            type: String,
            default: 'large',
        },

        colorButtons: {
            type: String,
            default: 'secondary',
        },
    },

    data() {
        return {
            current: this.index,
        };
    },

    watch: {
        index(val) {
            this.$nextTick(() => {
                this.current = val;
            });
        },
    },
};
</script>

<style lang="scss" module>
    .VNavigation {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .btn {
        &:first-child {
            margin-right: .8rem;
        }
    }
</style>
