<template>
    <div :class="[$style.IndexHero, 'container']">
        <IndexHeroSlider
            :class="$style.slider"
            :slides="slides"
        />

        <IndexHeroBanner :class="$style.banner"/>

        <IndexHeroFeatures :class="$style.benefits" />
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import IndexHeroSlider from '~/components/pages/index/hero/IndexHeroSlider.vue';
import IndexHeroFeatures from '~/components/pages/index/hero/IndexHeroFeatures.vue';
import { intersectionMixin } from '~/mixins/intersectionMixin.js';
import IndexHeroBanner from '~/components/pages/index/hero/IndexHeroBanner.vue';

export default {
    name: 'IndexHero',

    components: { IndexHeroBanner, IndexHeroFeatures, IndexHeroSlider },

    mixins: [intersectionMixin],

    props: {
        slides: {
            type: Array,
            default: () => [],
        },
    },

    watch: {
        isVisible() {
            if (this.isVisible) {
                history.replaceState({}, '', '/');
                this.changeActiveItem('');
            }
        },
    },

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
        }),
    },
};
</script>

<style lang="scss" module>
    .IndexHero {
        display: grid;
        grid-template-columns: 1fr 42.4rem;
        gap: 2rem;
        padding-top: 3.2rem;
        padding-bottom: 6.4rem;

        .banner {
            display: none;
        }

        @include respond-to(tablet) {
            grid-template-columns: 1fr;
            padding-top: 0;
            padding-bottom: 3.2rem;
        }

        @include respond-to(mobile) {
            gap: 0;

            .banner {
                display: flex;
                margin: 0 calc($aside-padding-mobile * -1) 3.2rem;
            }
        }
    }
</style>
