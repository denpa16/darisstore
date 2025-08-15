<template>
    <div
        :class="[$style.VMediaSlide, {[$style._shadows]: shadows}]"
        :style="{backgroundImage: firstSlideBackground}"
    >
        <video
            v-if="video"
            ref="video"
            :class="['lazy', 'swiper-slide', $style.image]"
            :data-src="video"
            autoplay="autoplay"
            playsinline="playsinline"
            :data-poster="previewImg"
            muted="muted"
            webkit-playsinline
            preload="none"
            @ended="onVideoEnded"
        />

        <img
            v-else
            :class="['lazy', 'swiper-slide', $style.image]"
            :alt="title"
            v-bind="ImgAttrs"
        />

        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'VMediaSlide',

    props: {
        slideIndex: {
            type: Number,
            default: 0,
        },

        video: {
            type: String,
            default: '',
        },

        image: {
            type: String,
            required: true,
        },

        active: {
            type: Boolean,
            default: false,
        },

        title: {
            type: String,
            default: 'image',
        },

        shadows: {
            type: Boolean,
            default: true,
        },

        prePreview: {
            type: String,
            default: 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
        },

        breakpoints: {
            type: String,
            default: 'mobile:100vw tablet:100vw laptop:100vw desktop:100vw',
        },

        loadFirstImg: Boolean,
    },

    data() {
        return {
            // Бэкграунд нужен только для первого слайда,
            // если слайдер находится на первом экране.
            firstSlideBackground: '',
        };
    },

    computed: {
        ImgAttrs() {
            const propsAttrs = {};

            if (this.loadFirstImg && this.slideIndex === 0) {
                propsAttrs['sizes'] = this.sizeOptions.sizes;
                propsAttrs['srcset'] = this.sizeOptions.srcset;

                return { src: this.image, ...propsAttrs };
            }

            propsAttrs['data-src'] = this.previewImg;
            propsAttrs['data-lazy-src'] = this.image;
            propsAttrs['data-lazy-sizes'] = this.sizeOptions.sizes;
            propsAttrs['data-lazy-srcset'] = this.sizeOptions.srcset;

            return { src: this.prePreview, ...propsAttrs };
        },

        sizeOptions() {
            const options = {
                sizes: this.breakpoints,
            };

            return this.$img.getSizes(this.image, options);
        },

        previewImg() {
            const options = {
                width: 400,
                quality: 40,
                blur: 60,
            };

            return this.$img(this.image, options);
        },
    },

    watch: {
        active: {
            immediate: true,
            handler: function(val) {
                this.$nextTick(() => {
                    if (!this.$refs.video) {
                        return;
                    }

                    val ? this.handlePlayVideo() : this.handlePauseVideo();
                });
            },
        },
    },

    created() {
        // Если слайдер находиться на первом экране (loadFirstImg), то засовываем превью в background,
        // чтобы пока грузиться основное изображение, показывалось превью
        if (this.loadFirstImg && this.slideIndex === 0) {
            this.firstSlideBackground = `url(${this.previewImg})`;
        }
    },

    methods: {
        handlePlayVideo() {
            this.$refs.video.play();
        },

        handlePauseVideo() {
            const player = this.$refs.video;
            player.pause();

            setTimeout(() => {
                player.currentTime = 0;
            }, 300);
        },

        onVideoEnded() {
            this.handlePauseVideo();
            this.$emit('video-ended');
        },
    },
};
</script>

<style lang="scss" module>
    .VMediaSlide {
        position: relative;
        display: block;
        width: 100%;
        height: 100%;
        background-size: cover;
        transform: translateZ(0);

        &._shadows {
            &:after {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                background: linear-gradient(rgba(0 0 0 / 90%) 0%, rgba(0 0 0 / 10%));
            }
        }
    }

    img.image,
    video.image {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
</style>
