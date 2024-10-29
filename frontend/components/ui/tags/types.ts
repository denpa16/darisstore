import type { TIconSize } from '~/components/ui/icon/types';
import type { ColorsEnum, SizeEnum } from '@/types/ui/type.ts';

export interface VTagProps {
    /**
     * Определяет тэг обертки
     */
    tag?: 'NuxtLink' | 'a' | 'button' | 'span' | 'div';
    /**
     * Определяет роут для NuxtLink
     */
    to?: string;
    /**
     * Определяет ссылку
     */
    href?: string;
    target?: string;
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: SizeEnum.large | SizeEnum.medium;
    /**
     * Определяет иконку в начале
     */
    iconBefore?: string;
    /**
     * Определяет иконку в конце
     */
    iconAfter?: string;
    /**
     * Определяет размер иконки
     */
    iconSize?: TIconSize;
    /**
     * Определяет текст тултипа
     */
    info?: string;
    /**
     * Определяет цвет лейбла
     */
    color?: ColorsEnum;
    /**
     * Определяет текст лейбла
     */
    label?: string | number;
    /**
     * Определяет возможность закрыть тег по клику на иконку
     */
    isChips?: boolean;
    disabled?: boolean;
}

export interface VSaleTagProps extends VTagProps {
    /**
     * Определяет текст в шилде акции
     */
    saleLabel?: string;
    /**
     * Определяет текст
     */
    text?: string;
    isGarland?: boolean;
}
