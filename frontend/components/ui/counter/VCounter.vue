<template>
    <span :class="$style.VCounter">
        <span ref="counterRef">0</span>{{ append }}
    </span>
</template>

<script>
import { gsap } from 'gsap';

export default {
    name: 'VCounter',

    props: {
        value: {
            type: Number,
            required: true,
        },

        step: {
            type: Number,
            default: 1,
        },

        duration: {
            type: Number,
            default: 1000,
        },

        initialValue: {
            type: Number,
            default: 0,
        },

        append: {
            type: String,
            default: '',
        },
    },

    watch: {
        value() {
            this.runAnimation();
        },
    },

    mounted() {
        this.$nextTick(() => {
            this.runAnimation();
        });
    },

    methods: {
        runAnimation() {
            gsap
                .to(this.$refs.counterRef, {
                    innerText: this.value,
                    duration: this.duration / 1000,
                    snap: {
                        innerText: this.step,
                    },
                });
        },
    },
};
</script>

<style lang="scss" module>
    .VCounter {
        //
    }
</style>
