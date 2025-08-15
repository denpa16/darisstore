<template>
    <VSection :class="$style.OurCoaches" title="НАШИ ТРЕНЕРЫ">
        <div :class="$style.list">
            <CoachCard
                v-for="coach in coachesList"
                :key="coach.slug"
                :coach="coach"
            />
        </div>
    </VSection>
</template>

<script>
import CoachCard from '~/components/pages/index/coaches/CoachCard.vue';
import { coaches } from '~/assets/js/constants/coaches.js';

export default {
    name: 'OurCoaches',

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
    .OurCoaches {
        //
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
