<script setup lang="ts">
// Types
import type { NavigationProps } from '~/components/sliders/types.ts';

// Components
import VButton from '~/components/ui/button/VButton.vue';

const $style = useCssModule();

// Types
const {
    min = 0,
    max = 0,
    index = 0,
    loop = false,
    colorButtons = 'primary',
    disabled = false,
    showCount = true,
    isCountBackground = false,
    sizeButtons = 'medium',
    sizeCount = '',
    isAddLeadingZero = false,
    sizeIcon = 'medium',
    colorCount = '',
} = defineProps<NavigationProps>();

const nextRef = ref<HTMLDivElement | null>(null);
const prevRef = ref<HTMLDivElement | null>(null);

defineExpose({
    nextRef,
    prevRef,
});

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${sizeCount}`]]: sizeCount,
        [$style[`_${colorCount}`]]: colorCount,
        [$style._count]: showCount,
        [$style._countBackground]: isCountBackground,
    },
]);

const navigationValue = computed(() => {
    const indexVal = index + 1;
    const maxVal = max + 1;

    if (isAddLeadingZero) {
        return {
            index: formatNumber(indexVal),
            max: formatNumber(maxVal),
        };
    }

    return {
        index: indexVal,
        max: maxVal,
    };
});
// #endregion

// #region Computed
function formatNumber(value: number): string {
    if (value >= 1 && value <= 9) {
        return `0${value}`;
    } else {
        return value.toString();
    }
}
// #endregion
</script>

<template>
    <div :class="[$style.Navigation, classList]">
        <div
            v-if="showCount"
            :class="['navigation-count', $style.count]"
        >
            <span :class="$style.val">
                {{ navigationValue.index }}
            </span>

            <span :class="$style.slash">
            </span>
            <span :class="$style.slashText">/</span>

            <span :class="$style.val">
                {{ navigationValue.max }}
            </span>
        </div>

        <VButton
            ref="prevRef"
            :class="['nav-prev', $style.btn]"
            :color="colorButtons"
            :size="sizeButtons"
            :disabled="disabled || (!loop && index === min)"
            round
            equal
        >
            <VIcon
                name="mock-arrow"
                :size="sizeIcon"
            />
        </VButton>
        <VButton
            ref="nextRef"
            :class="['nav-next', $style.btn]"
            :color="colorButtons"
            :size="sizeButtons"
            :disabled="disabled || (!loop && index === max)"
            round
            equal
        >
            <VIcon
                name="mock-arrow"
                :size="sizeIcon"
            />
        </VButton>
    </div>
</template>

<style lang="scss" module>
    .Navigation {
        display: flex;
        align-items: center;
        justify-content: center;

        &._count {
            .btn {
                &:global(.nav-prev) {
                    margin-right: .4rem;
                }
            }
        }

        &._countBackground {
            .count {
                padding: .2rem 1rem;
                border-radius: 5rem;
                background-color: #3e505d;
            }
        }

        &._small {
            .count {
                @include text(l3-regular);
            }

            .slash {
                display: none;
            }

            .slashText {
                display: block;
            }
        }

        &._whiteAndLightGray {
            .val {
                color: $base-0;

                &:last-child {
                    color: rgba($base-0, .4);
                }
            }

            .slash {
                background-color: rgba($base-0, .4);
            }

            .slashText {
                color: rgba($base-0, .4);
            }
        }
    }

    .btn {
        &:global(.nav-prev) {
            margin-right: .8rem;

            svg {
                transform: rotate(180deg);
            }

            @include respond-to(mobile) {
                margin-right: 12px;
            }
        }
    }

    .count {
        position: relative;
        display: flex;
        align-items: center;
        font-size: 2.4rem;
        font-weight: 500;
    }

    .val {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2em;
        height: 2em;
    }

    .slash {
        width: .2rem;
        height: 3.2rem;
        border-radius: 5px;
        background-color: currentcolor;
        transform: rotate(24deg);
    }

    .slashText {
        display: none;
    }
</style>
