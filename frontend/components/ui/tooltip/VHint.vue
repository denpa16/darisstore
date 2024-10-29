<script setup lang="ts">
/**
 * Пример компонента, содержащего контент, отображаемый внутри тултипа.
 * Рекомендуется создавать отдельный компонент под конкретную задачу.
 */
// #region Imports
import type { IHint } from './types.ts';
// #endregion

// #region Props
const {
    hint,
    theme = 'light',
    reverse = false,
} = defineProps<IHint>();
// #endregion

// #region Data
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style._reverse]: reverse,
    },
]);
// #endregion
</script>

<template>
    <div v-if="hint" :class="[$style.VHint, classList]">
        <div
            v-if="hint.image"
            :class="$style.image"
        >
            <img
                :src="hint.image"
                :alt="hint.title"
            />

        </div>

        <div :class="$style.content">
            <div
                v-if="hint.title"
                :class="$style.title"
                v-html="hint.title"
            />
            <div
                v-if="hint.text"
                :class="$style.text"
                v-html="hint.text"
            />
            <template v-if="hint.tags">
                <div
                    v-for="(tag, idx) in hint.tags"
                    :key="'tag-' + idx"
                    :class="$style.tag"
                >
                    <div
                        v-if="tag.title"
                        :class="$style.title"
                        v-html="tag.title"
                    />
                    <div
                        v-if="tag.text"
                        :class="$style.text"
                        v-html="tag.text"
                    />
                </div>
            </template>

            <div
                v-if="hint.link"
                :class="$style.link"
            >
                <VLink
                    :to="hint.link"
                    :theme="theme"
                    size="small"
                    :disabled="false"
                    :active="false"
                    :has-arrow="true"
                >
                    Label
                </VLink>
            </div>
        </div>

    </div>
</template>

<style lang="scss" module>
    .VHint {
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 22.5rem;
        border-radius: 1.2rem;

        /** Themes */
        &._light {
            background-color: $base-0;
            color: $base-600;
            box-shadow: 0 .4rem 3.8rem 0 rgba(21 22 24 / 8%);
        }

        &._dark {
            background-color: rgba($base-600, .8);
            color: $base-0;
            backdrop-filter: blur(4px);
        }

        /** End Colors */

        &._reverse {
            flex-direction: column-reverse;
        }
    }

    .content {
        padding: 1.6rem;
    }

    .image {
        overflow: hidden;
        width: 100%;
        height: 14rem;
        background: $base-400;

        img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    .tag {
        &:not(:first-child) {
            margin-top: 1.6rem;
        }
    }

    .title {
        @include text(l3-regular);

        &:not(:first-child) {
            margin-top: 1.6rem;
        }
    }

    .text {
        @include text(p4);

        &:not(:first-child) {
            margin-top: .8rem;
        }

        > p {
            @include text(p4);
        }
    }

    .link {
        margin-top: 1.6rem;
    }
</style>
