<template>
    <div :class="[$style.index, 'container']">
        <h1 :class="$style.title">НАШИ ТРЕНЕРЫ</h1>


        <div :class="$style.list">
            <CoachCard
                v-for="coach in coachesList"
                :key="coach.slug"
                :coach="coach"
            />
        </div>
    </div>
</template>

<script>
import CoachCard from '~/components/pages/index/coaches/CoachCard.vue';
import { coaches } from '~/assets/js/constants/coaches.js';

export default {
    name: 'Index',

    components: { CoachCard },

    computed: {
        coachesList() {
            return coaches;
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .index {
        padding-bottom: 10rem;

        @include respond-to(mobile) {
            padding-bottom: 2.4rem;
        }
    }

    .title {
        @include text(h2);

        margin: 4rem 0;
        text-transform: uppercase;

        @include respond-to(mobile) {
            @include text(h4);

            margin-bottom: 3.2rem;
        }
    }

    .list {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.6rem;

        @include respond-to(tablet) {
            grid-template-columns: repeat(2, 1fr);
        }

        @include respond-to(mobile) {
            grid-template-columns: 1fr;
        }
    }
</style>
