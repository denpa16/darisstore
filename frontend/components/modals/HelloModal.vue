<script setup
        lang="ts"
>

// #region Vue
// Types
import type { HelloProps } from './types.ts';
// #endregion


// #region Props
const {
    title = '',
    description = '',
} = defineProps<HelloProps>();
// #endregion

// #region Data
const count = ref<number>(1);
// #endregion
</script>


<template>
    <div :class="$style.HelloModal">
        <div :class="$style.wrapper">
            <h3
                v-if="title"
                :class="$style.title"
            >
                {{ title }} {{ count }}
            </h3>

            <p
                v-if="description"
                :class="$style.description"
                v-html="description"
            />

            <!--            <button-->
            <!--                :class="$style.button"-->
            <!--                @click="openHelloModal"-->
            <!--            >-->
            <!--                Open another one modal-->
            <!--            </button>-->
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    .HelloModal {
        display: flex;
        justify-content: center;
        padding-top: 4rem;
    }

    .title {
        text-align: center;
    }

    .description {
        margin-top: $aside-padding;
        text-align: center;
    }

    .button {
        margin-top: 2rem;
        padding: 1.2rem;
        border-radius: 1rem;
        background: #e4e4e4;
        font-size: 1.2rem;
        transition: opacity .3s;
        cursor: pointer;
        user-select: none;

        @mixin hover {
            opacity: .7;
        }
    }
</style>
