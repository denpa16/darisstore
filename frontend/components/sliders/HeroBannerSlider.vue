<script setup lang="ts">

// Types
import type { Swiper, SwiperOptions } from 'swiper/types';
import type { HeroBannerSliderProps } from '~/components/sliders/types';

// Composables
import { useSlider } from '~/composables/slider/useSlider';

// Components
import MediaSlide from '~/components/sliders/MediaSlide.vue';
import Navigation from '~/components/sliders/Navigation.vue';

// Props
const {
    gallery = [],
    slideEffect = 'slide',
    autoplayDelay = 8000,
    sizes, // mobile:100vw tablet:100vw laptop:100vw desktop:100vw,
    withMenu = false,
    firstBlock,
    shadowsPosition,
} = defineProps<HeroBannerSliderProps>();


// Modules
const { $swiper, $swiperModules } = useNuxtApp();

const slider = ref<Swiper | null>(null);
const sliderRef = ref<HTMLElement | null>(null);
const navigationRef = ref<HTMLElement | null>(null);
const paginationRef = ref<HTMLElement | null>(null);
const activeIndex = ref<number>(0);
const direction = ref<string>('next');
const speedChangeSlides = ref<number>(400);
const $style = useCssModule();

const classList = computed(() => ({
    [$style[`_${direction.value}`]]: direction.value,
    [$style._menu]: withMenu,
}));

const activeSlide = computed(() => gallery?.length ? gallery[activeIndex.value] : null);

const {
    handleChangeSliderAutoplay,
    handleVideoEnded,
} = useSlider({ slider, activeSlide, autoplay: true });

/**
 * Инициализация swiper, в случае наличия нескольких слайдов
 * @public
 */
function handleInitSlider() {
    const options: SwiperOptions = {
        /**
         * Активация модулей свайпера,
         * все доступные см. frontend/config/plugins/swiper.js
         */
        modules: [
            $swiperModules.Navigation,
            $swiperModules.Pagination,
            $swiperModules.Autoplay,
        ],

        /**
         * Логика для навигации подвешивается на кнопки.
         * ! Важно ! при использовании nuxt-components с текущим конфигом,
         * они не будут присутствовать в dom, по этому импортируйте их вручную
         */
        navigation: {
            nextEl: navigationRef.value?.nextRef?.$el,
            prevEl: navigationRef.value?.prevRef?.$el,
        },

        /**
         * Настройки модуля пагинации
         */
        pagination: {
            el: paginationRef.value,
            type: 'bullets',
            bulletClass: 'hero-slider-bullet',
            bulletActiveClass: 'is-active',
            clickable: true,
            dynamicBullets: false,
        },

        /**
         * Настройки модуля autoplay, при инициализации стоит на паузе,
         * пока не произойдёт загрузка первого слайда из lazyload
         */
        autoplay: {
            delay: autoplayDelay,
            disableOnInteraction: false,
        },

        effect: slideEffect as 'slide' | 'fade' | 'cube' | 'coverflow' | 'flip' | 'creative' | 'cards',
        loop: true,
        slidesPerView: 1,
        simulateTouch: false,
        observer: true,
        speed: speedChangeSlides.value,

        // Callbacks
        on: {
            /**
             * Фиксируем текущий слайд, необходимо для видео
             * и отображения текстового контента / кнопок слайда
             */
            slideChange: swiper => {
                activeIndex.value = swiper.realIndex;
            },

            /**
             * Определение направления переключения слайда,
             * используется для transition анимации типа slide
             */
            slidePrevTransitionStart: () => {
                direction.value = 'prev';
            },

            slideNextTransitionStart: () => {
                direction.value = 'next';
            },

            /**
             * Отключение авто-переключения слайда для видео,
             * ждём завершения воспроизведения
             */
            slideChangeTransitionEnd: swiper => {
                handleChangeSliderAutoplay(swiper);
            },
        },
    };

    if (slideEffect === 'fade') {
        options.modules?.push($swiperModules.EffectFade);
    }

    slider.value = new $swiper(sliderRef.value as HTMLElement, options);
}


onMounted(async () => {
    await nextTick();
    handleInitSlider();
});

onBeforeUnmount(() => {
    if (slider.value) {
        slider.value?.destroy();
    }
});
</script>

<template>
    <section :class="[$style.HeroBannerSlider, classList]">
        <div
            v-if="gallery && gallery.length"
            ref="sliderRef"
            :class="['swiper-container', $style.slider]"
        >
            <div class="swiper-wrapper">
                <MediaSlide
                    v-for="(slide, index) of gallery"
                    :key="slide.id"
                    :slide-index="index"
                    :active="index === activeIndex"
                    :image="slide.image"
                    :title="slide.title"
                    :video="slide.video"
                    :sizes="sizes"
                    :shadows-position="shadowsPosition"
                    class="swiper-slide"
                    :load-first-img="firstBlock"
                    @video-ended="handleVideoEnded"
                />
            </div>
        </div>

        <div :class="$style.paginationContainer">
            <div
                ref="paginationRef"
                :class="$style.bullets"
                class="swiper-pagination"
            >
            </div>
        </div>

        <div
            v-if="gallery && gallery.length"
            :class="['container', $style.info]"
        >
            <div :class="$style.infoInner">
                <transition-group
                    :class="$style.infoContent"
                    :name="effect === 'slide' ? 'content-change' : 'fade-fast'"
                    tag="div"
                >
                    <div
                        v-for="(content, index) of gallery"
                        v-show="index === activeIndex"
                        :key="content.id"
                        :class="$style.infoContentSlide"
                    >
                        <div :class="$style.slideBottom">
                            <div
                                v-if="content.title"
                                :class="$style.slideBottomTitle"
                                v-html="content.title"
                            >
                            </div>

                            <div
                                v-if="content.subtitle"
                                :class="$style.slideBottomSubtitle"
                                v-html="content.subtitle"
                            >
                            </div>

                            <VButton
                                v-if="content.button_text && content.link"
                                tag="a"
                                target="_blank"
                                :href="content.link"
                                :class="$style.slideBottomButton"
                            >
                                {{ content.button_text }}
                            </VButton>
                        </div>
                    </div>
                </transition-group>

                <template v-if="gallery && gallery.length > 1">
                    <Navigation
                        ref="navigationRef"
                        :class="$style.navigation"
                        :max="gallery && gallery.length - 1"
                        :index="activeIndex"
                        show-count
                        size-buttons="small"
                        color-buttons="whiteFill"
                        loop
                    />
                </template>
            </div>
        </div>
    </section>
</template>

<style lang="scss" module>
    $base-0-color: $base-0;

    .HeroBannerSlider {
        position: relative;
        z-index: 0;
        overflow: hidden;
        width: 100%;
        height: 100dvh;
        min-height: 500px;
        color: $base-0-color;

        &._next,
        &._prev {
            .infoContentSlide {
                &:global(.content-change-enter-active),
                &:global(.content-change-leave-active) {
                    opacity: 1;
                }

                &:global(.content-change-enter-active) {
                    transition: opacity .3s ease-in .3s, transform .3s ease-in .3s;
                }

                &:global(.content-change-leave-active) {
                    transition: opacity .3s ease-in, transform .3s ease-in;
                }

                &:global(.content-change-enter),
                &:global(.content-change-leave-to) {
                    opacity: 0;

                    @include respond-to(mobile) {
                        transform: translate3d(0, 0, 0);
                    }
                }
            }
        }

        &._next {
            .infoContentSlide {
                &:global(.content-change-enter),
                &:global(.content-change-leave-to) {
                    transform: translate3d(2rem, 0, 0);
                }
            }
        }

        &._prev {
            .infoContentSlide {
                &:global(.content-change-enter),
                &:global(.content-change-leave-to) {
                    transform: translate3d(-2rem, 0, 0);
                }
            }
        }

        &._menu {
            height: calc(100vh - #{$header-h});
            margin-top: $header-h;

            @include respond-to(tablet) {
                height: calc(100vh - #{$header-h-tablet});
                margin-top: $header-h-tablet;
            }

            @include respond-to(mobile) {
                height: calc(100vh - #{$header-h-mobile});
                margin-top: $header-h-mobile;
            }
        }

        @include respond-to(mobile) {
            min-height: 640px;
        }

        .info {
            position: relative;
            z-index: 1;
            width: 100%;
            height: 100%;
            padding: 2.4rem 2.4rem 6.4rem ;
            pointer-events: none;

            @include respond-to(mobile) {
                padding-bottom: 48px;
            }
        }
    }

    .slider {
        user-select: none;

        &:global(.swiper-container) {
            position: absolute;
            inset: 0 0;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }

        :global(.swiper-wrapper) {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
    }

    .infoInner {
        position: relative;
        width: 100%;
        height: 100%;
        padding-top: $header-h;

        @include respond-to(mobile) {
            padding-top: $header-h-mobile;
        }
    }

    .infoContent {
        position: relative;
        width: 100%;
        height: 100%;
    }

    .infoContentSlide {
        position: absolute;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: space-between;
        width: 100%;
        height: 100%;
        transform: translate3d(0, 0, 0);
        flex-direction: column;

        @include respond-to(mobile) {
            right: auto;
            bottom: 0;
            left: 0;
            width: 100%;
            padding-bottom: 80px;
        }
    }

    .slideBottom {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        flex: 1;
    }

    .slideBottomTitle {
        width: 55%;
        font-size: 7.2rem;

        @include respond-to(mobile) {
            width: 85%;
            font-size: 3.2rem;
            line-height: 1.2;
        }
    }

    .slideBottomSubtitle {
        width: 40vw;
        margin-top: 2.4rem;
        font-size: 20px;
        line-height: 1.4;

        @include respond-to(mobile) {
            width: 55vw;
            margin-top: 1.2rem;
            font-size: 1.2rem;
            line-height: 1.33;
        }
    }

    .slideBottomButton {
        position: absolute;
        right: 20rem;
        bottom: 2px;
        pointer-events: all;

        @include respond-to(mobile) {
            right: 0;
            display: flex;
            justify-content: center;
            width: 100%;
        }
    }

    .paginationContainer {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        min-height: 6.4rem;

        @include respond-to(mobile) {
            min-height: 32px;
        }

        .bullets {
            &:global {
                &.swiper-pagination-horizontal.swiper-pagination-bullets {
                    position: absolute;
                    inset: 12px 0 0 0;
                    z-index: 20;
                    overflow: hidden;
                    margin: auto;
                    padding: 0 2px;
                    white-space: nowrap;
                    transform: translate3d(0, 0, 0) rotate(0);

                    .hero-slider-bullet {
                        position: relative;
                        display: inline-block;
                        width: 6px;
                        height: 6px;
                        border-radius: 50%;
                        background-color: $base-0-color;
                        opacity: .4;
                        transition: transform .25s ease, .25s left, opacity .3s ease;

                        &:not(:last-child) {
                            margin-right: 6px;
                        }

                        &.is-active {
                            opacity: 1;
                        }
                    }

                    @include respond-to(mobile) {
                        top: 0;
                    }
                }
            }

            @include respond-to(mobile) {
                display: block;
            }
        }
    }

    .navigation {
        position: absolute;
        right: 0;
        bottom: 0;
        pointer-events: all;

        @include respond-to(mobile) {
            display: none;
        }
    }
</style>
