import type { TTheme } from '~/types/ui/type';

export interface Props {
    /**
     * Определяет выбранный тэг
     */
    tag?:string;
    /**
     * Определяет url ссылки
     */
    to?: string | null | undefined,
    /**
     * Определяет свойство target сылки
     */
    target?: '_blank' | '_self' | '_top' | '_parent',
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: 'small' | 'medium'| 'large',
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    theme?: TTheme,
    /**
     * Определяет классы стилизации ссылок в зависимости от местонахождения
     */
    type?: 'link' | 'menuItem' | 'footerItem',
    /**
     * Активное состояние ссылки
     */
    active?: boolean,
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean,
    /**
     * Это свойство показывает, содержит ли ссылка иконку
     */
    hasArrow?: boolean,
    /**
     * Можно ли взаимодействовать со ссылкой если она уже активна
     */
    alwaysInteracting?: boolean,
}
