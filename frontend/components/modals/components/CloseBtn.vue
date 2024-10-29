<script lang="ts" setup>
// #region Props
const { color = 'black' } = defineProps<{ color?: string }>();
// #endregion

// #region Emits
const emits = defineEmits<{
    'close': []
}>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${color}`]]: color,
    },
]);
// #endregion

// #region Methods
function close() {
    emits('close');
}
// #endregion
</script>

<template>
    <button
        :class="[$style.CloseBtn, classList]"
        @click="close"
    >
        <VIcon name="mock-close" size="medium" />
    </button>
</template>

<style lang="scss" module>
    .CloseBtn {
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 4.8rem;
        height: 4.8rem;
        border-radius: 4.8rem;
        border: 1px solid $base-200;
        background: $base-0;
        color: $base-900;
        transition: $default-transition;
        cursor: pointer;

        @include respond-to(tablet) {
            width: 4rem;
            height: 4rem;
        }

        &:hover {
            border-color: $primary-900;
        }

        svg {
            width: 3rem;
            height: 3rem;

            @include respond-to(tablet) {
                width: 1.6rem;
                height: 1.6rem;
            }
        }
    }
</style>
