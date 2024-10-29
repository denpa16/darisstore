<script setup lang="ts">
// #region Imports
import { useMounted } from '@vueuse/core';
// #endregion

// #region Types
export interface TeleportProps {
    to?: string | HTMLElement;
    disabled?: boolean;
    forceMount?: boolean;
}

// #endregion

// #region Props
const {
    to = 'body',
    forceMount,
    disabled,
} = defineProps<TeleportProps>();
// #endregion

// #region Lifecycle
const isMounted = useMounted();
// #endregion
</script>

<template>
    <Teleport
        v-if="isMounted || forceMount"
        :to="to"
        :disabled="disabled"
    >
        <slot />
    </Teleport>
</template>
