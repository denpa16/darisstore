import type { TColor, TTheme } from '~/types/ui/type';

export interface Props {
    /**
     * Селектор элемента в который будет вставлен тултип.
     * Должен иметь свойство position: relative или  position: absolute
     */
    attach?: string;
    /**
     * Активирует позиционирование тултипа относительно контейнера
     */
    attachRelative?: boolean;
    top?: boolean;
    bottom?: boolean;
    left?: boolean;
    right?: boolean;
    // Располагать не по центра от активатора а по правому его краю
    rightToActivator?: boolean;
    hoverable?: boolean;
    isPopover?: boolean;
    disabled?: boolean;
    /**
     * Отступ от активатора до тултипа
     */
    nudge?: number;
    /**
     * Вертикальный отступ от краев экрана до тултипа
     * Позиционирование относительно контейнера, если attachRelative = true
     */
    offsetY?: number | string;
    /**
     * Горизонтальный отступ от краев экрана до тултипа
     * Позиционирование относительно контейнера, если attachRelative = true
     */
    offsetX?: number | string;
    text?: string;
    color?: Extract<TColor, 'primary'>;
    theme?: TTheme;
    tag?: 'div' | 'span';
}

type TTag = {
    title?: string,
    text?: string,
}

type THint = {
    title?: string | null,
    text?: string | null,
    image?: string | null,
    link?: string | null,
    tags?: TTag[] | null,
}

export interface IHint {
    hint: THint,
    theme?: TTheme,
    /**
     * Определяет местонахождение картинки
     */
    reverse?: boolean,
}

export interface VTooltipContainerProps {
    hasArrow?: boolean
    arrowPosition?: 'bottom' | 'topRight'
}
