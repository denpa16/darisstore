<script setup lang="ts">
// #region Types
import type { InputHintProps } from './types';
// #endregion

// #region Props
const {
    theme = 'light',
    absolute,
    disabled = false,
} = defineProps<InputHintProps>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style._absolute]: absolute,
        [$style._disabled]: disabled,
    },
]);
// #endregion

</script>

<template>
    <div :class="[$style.InputHint, classList]">
        <slot></slot>
    </div>
</template>

<style lang="scss" module>
    $grey-color: $base-400;
    $alert-color: $primary-900;
    $grey-light-color: $base-200;

    .InputHint {
        @include text(l3);

        position: relative;
        width: calc(100% - 2rem);
        margin-top: 1.2rem;

        &._absolute {
            position: absolute;
            top: calc(100% + 1.2rem);
            margin: 0;
        }

        /* Colors */
        &._light {
            color: $grey-color;

            &._disabled {
                color: $grey-light-color;
            }
        }

        &._dark {
            color: $grey-light-color;

            &._disabled {
                color: $grey-color;
            }
        }

        &._alert {
            color: $alert-color;
        }

        @include respond-to(mobile) {
            font-size: 1.2rem;
        }
    }
</style>
