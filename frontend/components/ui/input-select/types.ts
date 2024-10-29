import type { Choice } from '~/types/filter';
import type { TColor, TSize, TTheme } from '@/types/ui/type.ts';

export interface Props {
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'small' | 'medium'>;
    /**
     * Определяет классы, которые будут модифицировать тему
     */
    theme?: TTheme;
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>;
    /**
     * Лейбл инпута
     */
    label?: string,
    /**
     * Текущее введёное значение
     */
    modelValue?: string,
    /**
     * Позволяет отображать лейбл после ввода
     */
    keepLabel?: boolean,
    /**
     * Сообщение пользователю, может использоваться для валидации
     */
    msg?: string,
    /**
     * Модификатор вида с бордером
     */
    border?: boolean,
    /**
     * Модификатор поля ввода с невалидным значением
     */
    error?: boolean,
    /**
     * Даёт возможность отключить autocomplete при вводе
     */
    autocomplete?: boolean,
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean,
    /**
     * Массив значений в дропдауне
     * для каждого значения необходимы поля label и value
     */
    specs: Choice[]
}
