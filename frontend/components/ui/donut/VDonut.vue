<template>
    <div :class="$style.VDonut" :style="styles">
        <svg :viewBox="viewBox" :class="$style.donut">
            <circle
                :class="$style.hole"
                :cx="center"
                :cy="center"
                :r="radius"
                fill="transparent"
            />
            <circle
                :class="$style.ring"
                :cx="center"
                :cy="center"
                :r="radius"
                fill="transparent"
                :stroke-width="strokeWidth"
            />
            <circle
                :class="$style.segment"
                :cx="center"
                :cy="center"
                :r="radius"
                fill="transparent"
                :stroke-width="strokeWidth"
                :stroke-dasharray="dashValue"
                :stroke-dashoffset="dashOffset"
                stroke-linecap="round"
            />
        </svg>

        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'VDonut',

    props: {
        size: {
            type: Number,
            default: 40,
        },

        strokeWidth: {
            type: Number,
            default: 2,
        },

        value: {
            type: Number,
            required: true,
        },

        maxValue: {
            type: Number,
            default: 100,
        },

        startAngle: {
            type: Number,
            default: 0,
            validator: val => val >= 0 && val <= 359 || val <= 0 && val >= -359,
        },

        animationDuration: {
            type: Number,
            default: 1000,
        },

        transitionFunction: {
            type: String,
            default: 'ease',
            validator: val => ['linear', 'ease', 'ease-in', 'ease-out'].includes(val),
        },
    },

    computed: {
        viewBox() {
            return `0 0 ${this.size} ${this.size}`;
        },

        radius() {
            return (this.size - this.strokeWidth) / 2;
        },

        center() {
            return this.size / 2;
        },

        circumference() {
            return 2 * Math.PI * this.radius;
        },

        currentValue() {
            return this.value / this.maxValue * this.circumference;
        },

        dashValue() {
            return `${this.currentValue} ${this.circumference - this.currentValue}`;
        },

        dashOffset() {
            const degree = this.circumference / 360;
            const startPos = this.circumference / 4;

            if (this.startAngle < 0) {
                return startPos + degree * Math.abs(this.startAngle);
            }

            return startPos - degree * this.startAngle;
        },

        styles() {
            return {
                '--duration': `${this.animationDuration / 1000}s`,
                '--transition-function': this.transitionFunction,
            };
        },
    },
};
</script>

<style lang="scss" module>
    .VDonut {
        --donut-ring-color: #{$white};
        --donut-segment-color: #{$primary-500};

        .donut {
            width: 100%;
            height: 100%;
        }

        .ring {
            stroke: var(--donut-ring-color);
        }

        .segment {
            transform-origin: center;
            stroke: var(--donut-segment-color);
            transition: stroke-dasharray var(--duration) var(--transition-function);
            will-change: stroke-dasharray;
        }
    }
</style>
