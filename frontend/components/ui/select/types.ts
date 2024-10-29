import type { TColor, TSize, TTheme } from '~/types/ui/type';
import type {
    Choice,
    ChoiceLabel,
    ChoiceLabelKeyType,
    ChoiceValue,
    ChoiceValueKeyType,
} from '~/types/filter';

export interface OptionType extends Choice {
    disabled?: boolean;
    selected?: boolean;
    nextSelected?:boolean;
    inner_specs?: OptionType[];
    inner_facets?: ChoiceValue[];
}

export interface VSelectProps {
    /**
     * Имя ключа для работы с формами или запросами
     */
    name?: ChoiceLabel;
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'medium'>;
    /**
     * Определяет классы, которые будут модифицировать тему
     */
    theme?: TTheme | 'clear';
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>;
    /**
     * Текущее значение для определения активного элемента
     */
    modelValue?: ChoiceValue | ChoiceValue[] | null;
    /**
     * Название поля для value
     */
    valueName?: ChoiceValueKeyType;
    /**
     * Название поля для label
     */
    labelName?: ChoiceLabelKeyType;
    /**
     * Диапазон всех доступных значений селектора
     */
    specs: OptionType[];
    /**
     * Значения, которые доступны после передачи параметров в backend,
     * если существует определённый item в specs, но отсуствует в facets,
     * то по логике компонента, он перестаёт быть активным для выбора.
     */
    facets?: ChoiceValue[];
    /**
     * Значение, которое подставляется в селектор, визуально,
     * если в value является пустой переменной.
     */
    placeholder?: string;
    /**
     * Доп. элемент в селекторе, при выборе
     * которого - сбрасывается состояние value
     */
    resetLabel?: string;
    /**
     * Включает возможность выбора более одного элемента.
     */
    multiple?: boolean;
    /**
     * Скрывает выбранные варианты из селектора
     */
    hideSelected?: boolean;
    /**
     * Скрывает отфильтрованные варианты из селектора
     */
    hideFiltered?: boolean;
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean;
    /**
     * Запрещает сброс активного элемента
     */
    required?: boolean;
    /**
     * Можно передать название иконки svg-sprite, для отображения в поле ввода
     */
    prefixIcon?: string;
    info?: string;
    infoRight?: string;
    /**
     * Лейбл
     */
    label?: string;
    msg?: string;
    error?: boolean;
    /**
     * Отображать раскрытые опции без кнопки вызова
     */
    onlyOptions?: boolean;
    /**
     * Ключ для анимирования списка опций
     */
    animationListKey?: string;
    /**
     * Флаг наличия внутренних фильтров в опциях.
     * ВАЖНО: При активации требует указанных name и innerName
     */
    hasInner?: boolean;
    /**
     * Название параметра для фильтров внутри опций (напр. buildings для корпусов внутри проектов).
     */
    innerName?: ChoiceLabel,
    /**
     * Значение фильтра внутри опций
     */
    innerValue?: ChoiceValue | ChoiceValue[] | null;
    /**
     * Флаг множественного выбора внутри опций
     */
    innerMultiple?: boolean,
    /**
     * Наименование кнопки сброса внутреннего значения
     */
    innerResetLabel?: string,
    /**
     * Показывать модалку со списком опций на мобилке
     */
    mobileModal?: boolean,
    /**
     * Флаг фильтрования внутренними значениями внешних
     */
    innerFiltersOuter?: boolean,
    absoluteHint?: boolean,
}

export interface VSelectOptionProps {
    option: OptionType;
    value: ChoiceValue | ChoiceValue[];
    valueName?: ChoiceValueKeyType;
    labelName?: ChoiceLabelKeyType;
    size?: Extract<TSize, 'medium'>;
    isHighlighted?: boolean;
    multiple?: boolean;
    theme?: TTheme | 'clear',
    hasInner?: boolean;
    innerValue?: ChoiceValue | ChoiceValue[];
    innerMultiple?: boolean,
    innerResetLabel?: string,
    /**
     *  Показывает активность следующего элемента
     */
    nextSelected?: boolean;
}
