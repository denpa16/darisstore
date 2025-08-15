<template>
    <VSlider
        :class="[$style.IndexHeroSlider, {[$style._hasPromo]: hasPromo}]"
        :slides="slides"
        :autoplay-delay="autoplayDelay"
        :speed-change-slides="speedChangeSlides"
        :navigation="isFewSlides"
        :pagination="isFewSlides && !$deviceIs.pc"
        :image-prop-name="imagePropName"
        first-block
        disabled-shadow
        @change-slide="forcedResetCount = !forcedResetCount"
    >
        <template #slide-inner="{slide}">
            <div :class="$style.slide">
                <div :class="$style.headings">
                    <h2
                        v-if="slide?.title"
                        :class="$style.title"
                        v-html="slide?.title"
                    >
                    </h2>
                    <div
                        v-if="slide?.subtitle"
                        :class="$style.subtitle"
                        v-html="slide?.subtitle"
                    />
                </div>
            </div>
        </template>

        <template #container>
            <div :class="$style.footer">
                <VButton
                    :class="$style.button"
                    :href="whatsappLink"
                    :size="$deviceIs.pc ? 'large' : 'medium'"
                >
                    Записаться на тренировку
                </VButton>
            </div>
        </template>
    </VSlider>
</template>

<script>
import { WHATSAPP_LINK } from '~/assets/js/constants/index.js';
import { mapGetters } from 'vuex';

export default {
    name: 'IndexHeroSlider',

    props: {
        slides: {
            type: Array,
            default: () => [],
        },
    },

    data() {
        return {
            whatsappLink: WHATSAPP_LINK,

            timer: null,
            isTimeLeft: true,
            autoplayDelay: 6000,
            speedChangeSlides: 600,
            forcedResetCount: false,
        };
    },

    computed: {
        ...mapGetters({
            hasPromo: 'menu/getHasPromo',
        }),

        isFewSlides() {
            return this.slides?.length > 1;
        },

        imagePropName() {
            return this.$deviceIs.pc ? 'image' : 'mobile_image';
        },
    },
};
</script>

<style lang="scss" module>
    .IndexHeroSlider {
        width: 100%;
        height: 54rem;
        border-radius: 1.2rem;
        background-color: $base-900;

        @include respond-to(tablet) {
            width: calc(100% + 1.6rem * 2);
            height: calc(100svh - $header-h-mobile);
            margin: 0 -1.6rem;
            border-radius: 0;

            &._hasPromo {
                height: calc(100svh - $header-h-mobile - $promo-h-tablet);
            }
        }
    }

    .slide {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 2.4rem;

        @include respond-to(tablet) {
            padding: 2.7rem 1.6rem 1.6rem;
        }
    }

    .title {
        @include text(h1);

        border-bottom: 1px solid $white-32;
        text-transform: uppercase;

        @include respond-to(tablet) {
            @include text(h3);

            margin-top: 0;
            line-height: 1.15;
            letter-spacing: -.1rem;
        }
    }

    .subtitle {
        @include text(h4);

        margin-top: 2rem;
        text-transform: uppercase;

        @include respond-to(tablet) {
            @include text(h5);

            margin-top: 2rem;
        }
    }

    .footer {
        position: absolute;
        right: 2rem;
        bottom: 2rem;
        left: 2rem;
        z-index: 1;
        display: flex;
        align-items: center;

        @include respond-to(tablet) {
            right: 1.6rem;
            bottom: 3.2rem;
            left: 1.6rem;
            flex-wrap: wrap;
        }
    }

    .count {
        width: 5.6rem;
        height: 5.6rem;
        margin-right: 2.7rem;

        @include respond-to(tablet) {
            margin-right: 0;
            margin-bottom: 2rem;
        }
    }

    .button {
        @include respond-to(tablet) {
            width: 100%;
        }
    }
</style>
