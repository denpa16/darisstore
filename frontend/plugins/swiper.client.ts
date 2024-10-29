import {
    Swiper,
} from 'swiper';

import {
    Navigation,
    Scrollbar,
    Thumbs,
    Mousewheel,
    Autoplay,
    Pagination,
    FreeMode,
    EffectFade,
} from 'swiper/modules';

type SwiperModules = {
    Navigation: typeof Navigation
    Scrollbar: typeof Scrollbar
    Thumbs: typeof Thumbs
    Mousewheel: typeof Mousewheel
    Autoplay: typeof Autoplay
    Pagination: typeof Pagination
    FreeMode: typeof FreeMode
    EffectFade: typeof EffectFade
}

export default defineNuxtPlugin(() => {
    const swiperModules: SwiperModules = {
        Navigation,
        Scrollbar,
        Thumbs,
        Mousewheel,
        Autoplay,
        Pagination,
        FreeMode,
        EffectFade,
    };

    const swiper: typeof Swiper = Swiper;

    return {
        provide: {
            swiperModules,
            swiper,
        },
    };
});
