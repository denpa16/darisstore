<script setup lang="ts">
/**
 * Компонент-обертка для удобного использования иконок
 *
 * @version 1.0.1
 * @displayName VIcon
 */

// #region Imports
import type { TIconSize } from './types';

// #endregion

interface IProps {
    name: string;
    size?: TIconSize;
}

// #region Props
const props = withDefaults(defineProps<IProps>(), {
    size: 'medium',
});
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${props.size}`]]: props.size,
    },
]);
// #endregion
</script>

<template>
    <svg-icon
        :name="name"
        :class="[$style.VIcon, classList]"
    />
</template>

<style lang="scss" module>
    .VIcon {
        fill: currentcolor;

        &._xs {
            width: 1rem;
            height: 1rem;
        }

        &._small {
            width: 1.2rem;
            height: 1.2rem;
        }

        &._sMedium {
            width: 1.4rem;
            height: 1.4rem;
        }

        &._medium {
            width: 1.6rem;
            height: 1.6rem;
        }

        &._sLarge {
            width: 2rem;
            height: 2rem;
        }

        &._large {
            width: 2.4rem;
            height: 2.4rem;
        }

        &._xxLarge {
            width: 3.2rem;
            height: 3.2rem;
        }
    }
</style>
