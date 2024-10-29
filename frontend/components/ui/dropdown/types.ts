import type { Choice, ChoiceValue } from '~/types/filter';
import type { TIconSize } from '~/components/ui/icon/types';
import type { TColor, TSize } from '@/types/ui/type.ts';
type TTheme = 'light' | 'dark';

export interface DropDownMenuTriggerProps {
    /**
     * Определяет открыто содержимое или нет
     */
    isActive?: boolean;
    /**
     * Определяет валиден ли выбор внутри содержимого или нет
     */
    isValid?: boolean;
    /**
     * Определяет состояние disabled
     */
    disabled?: boolean;
    /**
     * Определяет тему
     */
    theme?: Extract<TTheme, 'light'>;
    /**
     * Определяет цвет
     */
    color?: Extract<TColor, 'primary'>;
    /**
     * Определяет лейбл для VDropDownMenuTrigger
     */
    label?: string;
}

export interface VDropDownSingleProps {
    name?: string;
    specs: Choice[];
    facets?: ChoiceValue[];
    value: ChoiceValue;
    size?: Extract<TSize, 'medium'>;
    label?: string,
    additionalLabelFilter?: (val: string) => string,
    sizeIconLeft?: TIconSize;
    sizeIconRight?: TIconSize;
    iconLeft?: string;
    iconRight?: string;
    disabled?: boolean;
    theme?: Extract<TTheme, 'light'>;
    color?: Extract<TColor, 'primary'>;
    isFullWidth?: boolean,
}
