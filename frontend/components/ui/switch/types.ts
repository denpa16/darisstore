import type { TColor, TSize, TTheme } from '@/types/ui/type.ts';

export interface Props {
    /**
     * Текущее значение чекбокса
     */
    modelValue?: Array<string | boolean> | string | boolean;
    /**
     * Имя, которое используется при отправке формы
     */
    name?: string,
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'medium' | 'large'>,
    /**
     * Определяет классы, которые будут модифицировать тему
     */
    theme?: Extract<TTheme, 'light' | 'dark'>,
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>,
    /**
     * Значение, которое используется при отправке формы, а также передается в value
     * при активации чекбокса
     */
    trueValue?: string|boolean,
    /**
     * False значение, которое используется при отправке формы, а также передается в value
     * при активации чекбокса
     */
    falseValue?: string|boolean,
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean
    /**
     * Тултип false значения
     */
    falseInfo?: string,
    /**
     * Тултип true значения
     */
    trueInfo?: string,
}
