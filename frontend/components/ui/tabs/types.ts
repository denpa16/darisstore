import type { TTheme } from '~/types/ui/type';
import type {
    Choice,
    ChoiceLabel,
    ChoiceLabelKeyType,
    ChoiceValue,
    ChoiceValueKeyType,
} from '~/types/filter';

export interface VTabBarProps {
    /**
     * Имя ключа для работы с формами или запросами
     */
    name?: ChoiceLabel,
    /**
     * HTML тег - обертка для табов
     */
    tag?: 'ul' | 'div';
    /**
     * HTML тег - обертка для таба
     */
    childTag?: 'li' | 'div';
    /**
     * Массив всех табов, каждый из которых может содержать параметры описанные в VTab,
     * а также обязательные параметры label и value
     */
    specs: Choice[];
    /**
     * Значения, которые доступны после передачи параметров в backend,
     * если существует определённый item в specs, но отсуствует в facets,
     * то по логике компонента, он перестаёт быть активным для выбора.
     */
    facets?: ChoiceValue[];
    /**
     * Название поля для value
     */
    valueName?: ChoiceValueKeyType;
    /**
     * Название поля для label
     */
    labelName?: ChoiceLabelKeyType;
    /**
     * Текущее значение для определения активного элемента
     */
    modelValue?: ChoiceValue | ChoiceValue[];
    /**
     * Модификатор для отображения активного перемещающегося фона при переключении табов.
     * ВНИМАНИЕ: Будет считать некорректно, при наличии margin между табами
     */
    slider?: boolean;
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: 'small' | 'medium';
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    theme?: TTheme;
    /**
     * Определяет стилизацию табов
     */
    close?: boolean;
    /**
     * Добавляет общий бордер для табов
     */
    border?: boolean;
    /**
     * Флаг выбора нескольких табов (не совместимо со свойством slider)
     */
    multiple?: boolean;
    /**
     * Увеличенные падинги
     */
    extraPad?: boolean;
    /**
     * Перенос табов
     */
    flexWrap?: boolean;
    /**
     * Растягивание на всю ширину
     */
    fullWidth?: boolean;
    fullWidthWrapper?: boolean;
    /**
     * Кнопка сброса
     */
    resetLabel?: string,
    /**
     * Обязательность наличия значения
     */
    required?: boolean,
    /**
     * Тень выбранных табов
     */
    hasShadow?: boolean,
}

export interface VTabProps {
    tab: Choice,
    active?: boolean,
    disabled?: boolean,
    tag?: string,
    slider?: boolean;
    size?: 'small' | 'medium';
    theme?: TTheme;
    close?: boolean;
    extraPad?: boolean;
}
