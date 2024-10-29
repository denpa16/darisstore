<script setup lang="ts">
// #region Imports
import type { VFilterModalProps } from '~/components/ui/filter/types.ts';
import VButton from '@/components/ui/button/VButton.vue';
// #endregion

// #region Props
const {
    title = 'Фильтр',
    btnText = 'Применить',
    resetVisible = false,
    btnVisible = true,
    resetText = 'Сбросить',
    innerModal,
} = defineProps<VFilterModalProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    back: [],
    reset: [],
    accept: [],
}>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style._innerModal]: innerModal,
        [$style._hideBtn]: !btnVisible,
    },
]);
// #endregion
</script>

<template>
    <div :class="[$style.VFilterModal, ...classList]">
        <div :class="$style.overlay" @click="emit('accept')"></div>
        <div :class="$style.content">
            <div :class="$style.head">
                <VButton
                    equal
                    round
                    border
                    :class="$style.headBack"
                    @click="emit('back')"
                >
                    <VIcon name="mock-arrow-left-s" />
                </VButton>

                <span :class="[$style.headTitle, {[$style._resetVisible]: resetVisible}]">{{ title }}</span>

                <VButton
                    round
                    border
                    :class="[$style.headReset, {[$style._resetVisible]: resetVisible}]"
                    @click="emit('reset')"
                >
                    <span>{{ resetText }}</span>
                    <VIcon
                        name="mock-close"
                        :class="$style.headResetIcn"
                    />
                </VButton>
            </div>

            <div :class="$style.body">
                <slot />
            </div>

            <div
                v-if="btnVisible"
                :class="$style.foot"
            >
                <VButton
                    round
                    full-width
                    :class="$style.footBtn"
                    @click="emit('accept')"
                >
                    <Transition name="fade" mode="out-in">
                        <span :key="btnText">{{ btnText }}</span>
                    </Transition>
                </VButton>
            </div>
        </div>
    </div>
</template>

<style lang='scss' module>
    .VFilterModal {
        --head-h: 6.4rem;
        --foot-h: 8.8rem;

        position: fixed;
        top: 0;
        left: 0;
        z-index: 200;
        width: 100%;
        height: 100%;

        &._innerModal {
            position: absolute;

            .content {
                width: 100%;
                height: 100%;
            }
        }

        &._hideBtn {
            .body {
                height: calc(100% - var(--head-h));
            }
        }
    }

    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba($base-600, .8);
    }

    .content {
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 47.8rem;
        height: calc(100% - 4rem);
        border-radius: 1.2rem 1.2rem 0 0;
        background-color: white;
        transform: translateX(-50%);

        @include respond-to(mobile) {
            width: 100%;
            height: 100%;
            border-radius: 0;
        }
    }

    .head {
        position: relative;
        display: flex;
        align-items: center;
        height: var(--head-h);
        padding: 0 2rem;
        border-bottom: 1px solid $base-200;
    }

    .headTitle {
        @include text(l2-regular);

        margin-left: 1.2rem;
        line-height: 130%;

        &._resetVisible {
            @include respond-to(mobile) {
                overflow: hidden;
                max-width: calc(100% - 19.8rem);
                text-overflow: ellipsis;
            }
        }
    }

    .headReset {
        margin-left: auto;
        opacity: 0;

        &._resetVisible {
            opacity: 1;
        }
    }

    .headResetIcn {
        color: $base-400;
    }

    .body {
        overflow: auto;
        display: flex;
        height: calc(100% - var(--head-h) - var(--foot-h));
        flex-direction: column;
    }

    .foot {
        display: flex;
        align-items: center;
        height: var(--foot-h);
        padding: 0 2rem;
    }
</style>
