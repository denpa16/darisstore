import type { Swiper } from 'swiper/types';

export function useSlider(options) {
    /**
     * Отключает autoplay, если текущий слайд - видео
     * @param {Object} swiper instance
     * @public
     */
    function handleChangeSliderAutoplay(swiper: Swiper) {
        if (!options.autoplay) {
            return;
        }

        if (options.activeSlide.value.video || options.activeSlide.value.video_mp4 || options.activeSlide.value.video_webm) {
            swiper.autoplay.pause();
        } else if (!swiper.autoplay.running) {
            swiper.autoplay.resume();
        }
    }

    /**
     * Вручную переключает на следующий слайд, через эмит @video-ended,
     * если видео проигралось до конца. Т.к. если это видео, то мы выключаем autoplay.
     * После смены слайда отработает метод handleChangeSliderAutoplay и запустит autoplay снова.
     * @public
     */
    function handleVideoEnded() {
        options.slider.value?.slideNext();
    }

    return {
        handleChangeSliderAutoplay,
        handleVideoEnded,
    };
}
