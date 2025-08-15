<template>
    <div :class="[$style.Overlay, classList]">
        <transition name="fade">
            <div
                v-if="isActive"
                :class="$style.blind"
                @click="$emit('touchstart')"
                @touchstart="$emit('touchstart')"
            >
                <div v-if="withFinger" :class="$style.prompt">
                    <VIcon
                        :class="$style.finger"
                        adaptive
                        name="finger"
                        size="large"
                    />
                    <div class="t3">
                        Двигайте<br>
                        движением пальцев
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'Overlay',

    props: {
        isActive: {
            type: Boolean,
            default: false,
        },

        withFinger: {
            type: Boolean,
            default: false,
        },

        isAbsolute: {
            type: Boolean,
            default: false,
        },
    },

    computed: {
        classList() {
            return {
                [this.$style._absolute]: this.isAbsolute,
                [this.$style._active]: this.isActive,
            };
        },
    },
};
</script>

<style lang="scss" module>
    .Overlay {
        pointer-events: none;

        &._absolute {
            .blind {
                position: absolute;
            }
        }

        &._active {
            pointer-events: auto;
        }
    }

    .blind {
        position: fixed;
        top: 0;
        left: 0;
        display: grid;
        place-content: center;
        width: 100%;
        height: 100%;
        background-color: rgb(0 0 0 / 40%);
    }

    .prompt {
        text-align: center;
        color: $white;
        transform: translateY(-44%);
    }

    .finger {
        margin-bottom: 1.6rem;
    }
</style>
