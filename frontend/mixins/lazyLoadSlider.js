import LazyLoad from 'vanilla-lazyload';

// Constants
const LAZY_OPTIONS = {
    threshold: 10,
    use_native: false,
    unobserve_completed: true,
    unobserve_entered: true,
    elements_selector: '.lazy',
};

export const lazyLoadSlider = {
    data() {
        return {
            lazyLoad: null, // Инстанс vanilla-lazyload
            firstLoad: false, // autoplay срабатывает только после загрузки первого изображения
        };
    },

    methods: {
        /**
        * Коллбэк обсервера, срабатывающий когда слайдер показывается на экране,
        * вызывает замену байтового изображения.
        * @param {Array} entries объекты появившиеся на экране
        * @public
        */
        handleSliderIntersect(entries) {
            if (this.slider && entries?.[0]?.isIntersecting) {
                this.handleInitLazyLoad(this.slider);
            }
        },

        /**
         * Отключает autoplay и инициирует vanilla-lazyLoad.
         * После подмены байтового изображения, подгружает превью,
         * затем в качестве коллбэка вызывает метод handleSecondLoad
         * @param {Object} swiper instance
         * @public
         */
        handleInitLazyLoad(swiper) {
            if (!this.$refs.slider || !swiper) {
                return;
            }

            if (!this.$refs.slider.querySelectorAll(LAZY_OPTIONS.elements_selector)?.length) {
                console.warn(this.$refs.slider);
                console.warn(`Не могу найти ни одного элемента "${LAZY_OPTIONS.elements_selector}", внутри контейнера. Возможно, компонент слайда подключен не явно (без import).`);
                return;
            }

            if (swiper?.params?.autoplay?.enabled) {
                swiper.autoplay.stop();
            }

            this.lazyLoad = new LazyLoad({
                ...LAZY_OPTIONS,
                callback_loaded: this.handleSecondLoad,
                container: this.$refs.slider,
            });
        },

        /**
         * Создаёт новый инстанс vanilla-lazyLoad,
         * чтобы заменить превью на полноценное изображение.
         * Также запускает swiper autoplay в коллбэке,
         * после первой, полноценной, загрузки изображения
         * @param {Element} el html элемент слайда
         * @public
         */
        handleSecondLoad(el) {
            const lazyOptions = {
                ...LAZY_OPTIONS,
                data_srcset: 'lazy-srcset',
                data_sizes: 'lazy-sizes',
            };

            if (el.dataset?.lazySrcset || el.dataset?.lazySrc) {
                LazyLoad.resetStatus(el);
                ['data-ll-status', 'data-src'].forEach(attribute => el.removeAttribute(attribute));
                LazyLoad.load(el, lazyOptions);
            }

            if (!this.firstLoad) {
                if (this.slider?.params?.autoplay?.enabled) {
                    this.slider.autoplay.start();
                }
                this.firstLoad = true;
            }
        },
    },
};
