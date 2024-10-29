<script setup lang="ts">
import CloseBtn from '@/components/modals/components/CloseBtn.vue';

import type { BaseModalProps } from '~/components/modals/types.ts';
import VScrollBox from '@/components/ui/scrollbox/VScrollBox.vue';

// #region Props
const {
    tag,
    withCloseBtn = true,
    smallContent,
    isfullscreen = false,
    center = false,
    color = 'black',
} = defineProps<BaseModalProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'close': [],
}>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const component = computed(() => tag || VScrollBox);
const classList = computed(() => [
    {
        [$style._overflow]: component.value === 'div',
        [$style._smallContent]: smallContent,
        [$style._fullscreen]: isfullscreen,
        [$style._center]: center,
    },
]);
// #endregion

// #region Methods
function closeModal() {
    emit('close');
}
// #endregion
</script>

<template>
    <component
        :is="component"
        :class="[$style.scrollbox, ...classList]"
        data-scroll-lock-scrollable
        resizable
    >
        <div :class="$style.BaseModal">
            <CloseBtn
                v-if="withCloseBtn"
                :class="$style.close"
                :color="color"
                @click="closeModal"
            />

            <slot />
        </div>
    </component>
</template>

<style module lang="scss">
    .scrollbox {
        width: 56rem;
        max-height: calc(100dvh - .8rem);
        margin-top: .8rem;
        border-radius: 1.2rem;
        background-color: $base-0;

        @include respond-to(tablet) {
            width: 47.8rem;
            max-height: calc(100dvh - .8rem);
            margin-top: .8rem;
            border-radius: 1.2rem 1.2rem 0 0;
        }

        @include respond-to(mobile) {
            width: 100vw;
            max-height: none;
            margin-top: 0;
            border-radius: 0;
        }

        &._overflow {
            height: auto;
            max-height: none;
            margin: 0;

            @include respond-to(tablet) {
                overflow: auto;
                height: calc(100dvh - 4rem);
            }

            @include respond-to(mobile) {
                overflow: visible;
                height: auto;
            }
        }

        &._center {
            height: fit-content;
            max-height: none;
            margin: auto 0;

            @include respond-to(tablet) {
                overflow: auto;
                height: calc(100dvh - 4rem);
                margin: 0;
            }

            @include respond-to(mobile) {
                overflow: visible;
                height: auto;
            }
        }

        &._smallContent {
            @include respond-to(mobile) {
                border-radius: 1.2rem 1.2rem 0 0;
            }
        }

        &._fullscreen {
            width: 100vw;
            height: 100vh;
            margin: 0;

            .BaseModal {
                width: 100%;
                height: 100%;
                padding: 0;
            }
        }
    }

    .BaseModal {
        position: relative;
        padding: 6.8rem 4.8rem 4.8rem;

        @include respond-to(tablet) {
            padding: 2.2rem 2rem 2rem;
        }
    }

    .close {
        position: absolute;
        top: 2rem;
        right: 2rem;

        @include respond-to(tablet) {
            top: 1.2rem;
        }
    }
</style>
