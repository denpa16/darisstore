<script setup lang="ts">
</script>

<template>
    <div
        id="app"
        :class="$style.EmptyLayout"
    >
        <main :class="$style.main">
            <slot />
        </main>
    </div>
</template>

<style lang="scss" module>
    .EmptyLayout {
        max-width: calc(100% - var(--lock-offset, 0));
    }

    .main {
        position: relative;
        min-height: stretch;
    }
</style>
