<script setup lang="ts">
// #region Imports
import type { IOverlay } from '~/components/common/types.ts';
// #endregion

// #region Props
const {
    isActive = false,
    withFinger = false,
    isAbsolute = false,
} = defineProps<IOverlay>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._absolute]: isAbsolute,
        [$style._active]: isActive,
    },
]);
// #endregion
</script>

<template>
    <div :class="[$style.Overlay, classList]">
        <transition name="fade-fast">
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
                        name="mock-finger"
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
        color: $base-0;
        transform: translateY(-44%);
    }

    .finger {
        margin-bottom: 1.6rem;
    }
</style>
