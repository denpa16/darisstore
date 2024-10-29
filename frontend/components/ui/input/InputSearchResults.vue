<script setup
        lang="ts"
>
// #region Types
import type { InputSearchResults } from './types';
// #endregion

// #region Props
const {
    results,
} = defineProps<InputSearchResults>();
// #endregion

// #region Emits
const emit = defineEmits<{
    'click': [values: object],
}>();
// #endregion

</script>

<template>
    <div :class="$style.InputSearchResults">
        <NuxtLink
            v-for="(result, idx) in results"
            :key="'search-result-' + idx"
            :to="result.url"
            target="_blank"
            :class="$style.searchItem"
            @click="emit('click', result)"
        >
            <span>{{ result.number }}, {{ result.project }}</span>
        </NuxtLink>
    </div>
</template>

<style lang="scss"
       module
>
    .InputSearchResults {
        display: flex;
        flex-direction: column;
        padding: 0 .8rem;
    }

    .searchItem {
        @include text(l3-regular);

        display: flex;
        padding: 1.8rem 1.2rem;
        border-radius: .8rem;
        background-color: $base-0;
        line-height: 1.3;
        color: $base-600;
        transition: background $default-transition;

        @include hover {
            &:hover {
                background-color: $base-100;
            }
        }
    }
</style>
