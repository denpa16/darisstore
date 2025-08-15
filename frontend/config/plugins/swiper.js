import Vue from 'vue';
import {
    Swiper,
    Navigation,
    Scrollbar,
    Thumbs,
    Mousewheel,
    Autoplay,
    Pagination,
    FreeMode,
    EffectFade,
} from 'swiper';

const swiper = {
    install(Vue, options) {
        Vue.prototype.$swiper = Swiper;
        Vue.prototype.$swiperModules = {
            Navigation,
            Scrollbar,
            Thumbs,
            Mousewheel,
            Autoplay,
            Pagination,
            FreeMode,
            EffectFade,
        };
    },
};

Vue.use(swiper);
