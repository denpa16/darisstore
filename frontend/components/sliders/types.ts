import type { ButtonColors } from '~/types/ui/type';
import type { TIconSize } from '~/components/ui/icon/types';

export type TShadowsPosition = 'both' | 'bottom' | null;

interface HeroBannerSliderProps {
    /**
     * Массив объектов с данными для слайдера,
     * ```
     * пример данных см. frontend/assets/mock/json/slides.json
     * ```
     */
    gallery: Array<object>,
    /**
     * Тип анимации перехода между слайдами
     * ! Внимание ! в данный момент некоректно работает с lazyLoad,
     * все изображения слайдера грузятся сразу же
     */
    slideEffect?: 'slide' | 'fade' | 'cube' | 'coverflow' | 'flip' | 'creative' | 'cards',
    /**
     * Время паузы перед переключением на следующий слайд
     */
    autoplayDelay?: number,
    /**
     * Размеры imgProxy, 100vw в данном случае равен размеру брейкпоинта каждого устройства,
     * которые являются общими для Nuxt Device is и Nuxt Images (nuxt.config.js)
     */
    sizes?: string,
    /**
     * В случае, если слайдер является первым блоком и меню не прозрачное,
     * то добавляется отступ равный размеру самого меню, под каждый тип устройства.
     * Плюс, меняется размер блока, с расчётом, чтобы он помещался на один экран,
     */
    withMenu?: boolean,
    /**
     * Добавление первого изображения в статику, без ленивой загрузки
     */
    firstBlock?: boolean,
    shadowsPosition?: TShadowsPosition,
}

interface MediaSLideProps {
    video?: string,
    image?: string | null,
    title?: string | null,
    sizes?: string,
    active?: boolean,
    slideIndex: number,
    shadowsPosition?: TShadowsPosition,
    loadFirstImg?: boolean,
}

interface NavigationProps {
    min?: number,
    max?: number,
    index: number,
    loop?: boolean,
    colorButtons?: ButtonColors,
    colorCount?: string | '',
    disabled?: boolean,
    showCount?: boolean,
    sizeButtons?: 'xSmall' | 'small' | 'medium' | 'large',
    sizeCount?: 'xSmall' | 'small' | 'medium' | 'large' | '',
    isAddLeadingZero?: boolean,
    sizeIcon?: TIconSize,
    isCountBackground?: boolean,
}

interface MenuSliderItem {
    number_of_rule: number,
    name: string | null,
    text: HTMLElement | string | null,
    name_label: string | null,
    menu_description: string | null,
}

interface MenuSliderProps {
    gallery: Array<MenuSliderItem>,
    slideEffect?: 'slide' | 'fade' | 'cube' | 'coverflow' | 'flip' | 'creative' | 'cards',
    loop?: boolean,
    slidesPerView?: number,
    simulateTouch?: boolean,
    observer?: boolean,
    spaceBetween?: number,
    isCountBackground?: boolean,
    gaAction?: () => void,
    isVisibleTab?: boolean,
}

interface CardSlide {
    key: string,
    url: string,
    hover?: string | null,
    viewBoxX?: number | null,
    viewBoxY?: number | null,
}

interface CardSliderProps {
    slides: Array<CardSlide> | [],
}

interface CardSliderScrollParams {
    scrollXStart: number | null,
    scrollXEnd: number | null,
    scrollYStart: number | null,
    scrollYEnd: number | null,
}

export type {
    HeroBannerSliderProps,
    MediaSLideProps,
    NavigationProps,
    MenuSliderProps,
    CardSlide,
    CardSliderProps,
    CardSliderScrollParams,
};
