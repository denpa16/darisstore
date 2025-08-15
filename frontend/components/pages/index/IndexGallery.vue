<template>
    <section :class="[$style.IndexGallery, 'container']">
        <VSlider
            :key="`slider_${$deviceIs.device}`"
            :class="$style.gallery"
            :slides="images"
            :pagination="!$deviceIs.pc"
            :counter="$deviceIs.pc"
            :navigation="$deviceIs.pc"
            size-buttons="medium"
        >
            <template #slide-inner>
                <h2
                    :class="$style.title"
                    v-html="title"
                />
            </template>
        </VSlider>
    </section>
</template>

<script>
export default {
    name: 'IndexGallery',

    props: {
        images: {
            type: Array,
            default: () => [],
        },
    },

    data() {
        return {
            title: '<span>Наши выдающиеся достижения</span>  которые&nbsp;мы&nbsp;пережили вместе <br> в&nbsp;нашем спортивном клубе',
        };
    },
};
</script>

<style
    lang="scss"
    module
>
    .IndexGallery {
        height: 100dvh;
        padding-top: 6.4rem;
        padding-bottom: 6.4rem;

        @include respond-to(tablet) {
            height: 70dvh;
            padding-top: 3.2rem;
            padding-bottom: 3.2rem;
        }

        @include respond-to(mobile) {
            height: 37.5rem;
            padding: 3.2rem 0;
        }
    }

    .gallery {
        overflow: hidden;
        width: 100%;
        height: 100%;
        border-radius: 1.2rem;
    }

    .title {
        @include text(h3);

        position: absolute;
        top: 4rem;
        left: 4rem;
        z-index: 5;
        max-width: 98.6rem;
        text-transform: uppercase;
        color: $white-50;

        & span {
            color: $white;
        }

        @include respond-to(tablet) {
            @include text(h5);

            top: 1.6rem;
            right: 1.6rem;
            left: 1.6rem;
        }
    }
</style>
