<template>
    <section :class="[$style.VSlider, classList]">
        <div
            v-if="slides && slides.length"
            ref="slider"
            v-intersect.once="{handler: handleSliderIntersect, options: {threshold: [0]}}"
            :class="[$style.swiper, 'swiper']"
        >
            <div class="swiper-wrapper">
                <VMediaSlide
                    v-for="(slide, index) of slides"
                    :key="slide.id"
                    :slide-index="index"
                    :active="index === activeIndex"
                    :image="slide[imagePropName || 'image']"
                    :title="slide.title"
                    :video="slide.video"
                    :breakpoints="breakpoints"
                    class="swiper-slide"
                    load-first-img
                    :shadows="!disabledShadow"
                    @video-ended="handleVideoEnded"
                >
                    <slot name="slide-inner" :slide="slide"></slot>
                </VMediaSlide>
            </div>

            <VNavigation
                v-if="navigation && slider"
                ref="navigationRef"
                :class="[$style.navigation, 'navigation']"
                :index="activeIndex"
                :max="slides.length - 1"
                :loop="loop"
                :size-buttons="sizeButtons"
                @next="changeSLide"
                @prev="changeSLide(true)"
            />

            <div v-show="pagination && slider" :class="[$style.pagination, 'pagination pagination__white']"/>

            <VTag v-if="counter && slider" :class="$style.counter">{{ activeIndex + 1 }} из {{ slides.length }}</VTag>

            <slot name="container"></slot>
        </div>
    </section>
</template>

<script>
// Mixins
import { lazyLoadSlider } from '~/mixins/lazyLoadSlider.js';

// Components
import VMediaSlide from '~/components/ui/slider/VMediaSlide.vue';
import VNavigation from '~/components/ui/slider/VNavigation.vue';

/**
 * Слайдер для Hero Banner на основе Swiper<br>
 *
 * @version 1.1.0
 * @displayName HeroBannerSlider
 */
export default {
    name: 'VSlider',

    components: {
        VMediaSlide,
        VNavigation,
    },

    mixins: [lazyLoadSlider],

    props: {
        /**
         * Массив объектов с данными для слайдера,
         * пример данных см. frontend/assets/mock/json/slides.json
         */
        slides: {
            type: Array,
            required: true,
            default: () => [],
        },

        /**
         * Имя пропса, который содержит линк на картинку
         */
        imagePropName: {
            type: String,
            default: 'image',
        },

        sizeButtons: {
            type: String,
            default: 'large',
        },

        /**
         * Тип анимации перехода между слайдами
         * ! Внимание ! в данный момент некоректно работает с lazyLoad,
         * все изображения слайдера грузятся сразу же
         */
        effect: {
            type: String,
            default: 'slide',
            validator: val => ['slide', 'fade'].includes(val),
        },

        /**
         * Время паузы перед переключением на следующий слайд
         */
        autoplayDelay: {
            type: Number,
            default: 6000,
        },

        speedChangeSlides: {
            type: Number,
            default: 400,
        },

        /**
         * Брейкпоинты imgProxy, 100vw в данном случае равен размеру брейкпоинта каждого устройства,
         * которые являются общими для Nuxt Device is и Nuxt Images (nuxt.config.js)
         */
        breakpoints: {
            type: String,
            default: 'mobile:100vw tablet:100vw laptop:100vw desktop:100vw',
        },

        /**
         * В случае, если слайдер является первым блоком и меню не прозрачное,
         * то добавляется отступ равный размеру самого меню, под каждый тип устройства.
         * Плюс, меняется размер блока, с расчётом, чтобы он помещался на один экран,
         */
        withMenu: Boolean,

        /**
         * Добавление первого изображения в статику, без ленивой загрузки
         */
        firstBlock: Boolean,

        disabledShadow: Boolean,

        loop: Boolean,
        navigation: Boolean,
        pagination: Boolean,
        counter: Boolean,

        options: {
            type: Object,
            default: () => ({}),
        },
    },

    data() {
        return {
            slider: null, // Инстанс swiper
            activeIndex: 0,
        };
    },

    computed: {
        classList() {
            return {
                [this.$style._menu]: this.withMenu,
            };
        },

        activeSlide() {
            return this.slides?.length ? this.slides[this.activeIndex] : null;
        },
    },

    mounted() {
        this.$nextTick(() => {
            this.handleInitSlider();
        });
    },

    beforeDestroy() {
        if (this.slider) {
            this.slider.destroy();
        }
    },

    methods: {
        /**
         * Инициализация swiper, в случае наличия нескольких слайдов
         * @public
         */
        handleInitSlider() {
            if (!this.$refs.slider || this.slides.length <= 1) {
                this.handleInitLazyLoad(null);
                return;
            }

            const options = {
                /**
                 * Активация модулей свайпера,
                 * все доступные см. frontend/config/plugins/swiper.js
                 */
                modules: [
                    this.$swiperModules.Navigation,
                    this.$swiperModules.Pagination,
                    this.$swiperModules.Autoplay,
                ],

                /**
                 * Настройки модуля autoplay, при инициализации стоит на паузе,
                 * пока не произойдёт загрузка первого слайда из lazyload
                 */
                autoplay: {
                    delay: this.autoplayDelay,
                    disableOnInteraction: false,
                },

                pagination: {
                    el: '.pagination',
                    bulletClass: 'pagination-bullet',
                    bulletActiveClass: 'pagination-bullet-active',
                },

                effect: this.effect,
                loop: this.loop,
                slidesPerView: 1,
                simulateTouch: false,
                observer: true,
                speed: this.speedChangeSlides,

                // Callbacks
                on: {
                    /**
                     * Фиксируем текущий слайд, необходимо для видео
                     * и отображения текстового контента / кнопок слайда
                     */
                    slideChange: swiper => {
                        this.activeIndex = swiper.realIndex;
                        this.$emit('change-slide', this.activeIndex);
                    },

                    /**
                     * Отключение авто-переключения слайда для видео,
                     * ждём завершения воспроизведения
                     */
                    slideChangeTransitionEnd: swiper => {
                        this.handleChangeSliderAutoplay(swiper);
                    },
                },

                ...this.options,
            };

            /**
             * Подключаем модуль для работы с fade анимацией
             */
            if (this.effect === 'fade') {
                options.modules.push(this.$swiperModules.EffectFade);
            }

            this.slider = new this.$swiper(this.$refs.slider, options);
        },

        /**
         * Отключает autoplay, если текущий слайд - видео
         * @param {Object} swiper instance
         * @public
         */
        handleChangeSliderAutoplay(swiper) {
            if (this.activeSlide?.video) {
                swiper.autoplay.stop();
            } else {
                swiper.autoplay.start();
            }
        },

        /**
         * Вручную переключает на следующий слайд, через эмит @video-ended,
         * если видео проигралось до конца. Т.к. если это видео, то мы выключаем autoplay.
         * После смены слайда отработает метод handleChangeSliderAutoplay и запустит autoplay снова.
         * @public
         */
        handleVideoEnded() {
            this.slider.slideNext();
        },

        changeSLide(isPrev) {
            if (isPrev) {
                this.slider?.slidePrev();
                this.$emit('nav-prev');
            } else {
                this.slider?.slideNext();
                this.$emit('nav-next');
            }
        },
    },
};
</script>

<style lang="scss" module>
    $white-color: $white;

    .VSlider {
        position: relative;
        z-index: 0;
        overflow: hidden;
        color: $white-color;

        .swiper {
            position: absolute;
            inset: 0;
        }

        .counter,
        .pagination,
        .navigation {
            position: absolute;
            z-index: 5;
        }

        .navigation {
            right: 2rem;
            bottom: 2rem;

            @include respond-to(tablet) {
                display: none;
            }
        }

        .pagination {
            bottom: 2.4rem;

            @include respond-to(tablet) {
                bottom: 1.6rem;
            }
        }

        .counter {
            top: 2.4rem;
            right: 2.4rem;

            @include respond-to(tablet) {
                top: 1.6rem;
                right: 1.6rem;
            }
        }
    }
</style>
