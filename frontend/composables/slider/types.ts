import type { Swiper } from 'swiper/types';

interface ISliderOptions {
    slider: Swiper | null,
    sliderRef: HTMLElement | null,
    activeSlide: object,
    autoplay: boolean

}

export type {
    ISliderOptions,
};
