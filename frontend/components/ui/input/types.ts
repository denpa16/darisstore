import type { TColor, TSize, TTheme } from '~/types/ui/type';

interface SearchItem {
    url?: string;
    number?: number;
    project?: string;
}

type AutocompleteNameType = 'off'|'on'|'one-time-code'|'name'|'family-name'|'additional-name'|'tel'|'email'

export interface InputProps {
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'medium'>,
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>;
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    theme?: TTheme;
    /**
     * Тип, для передачи в атрибуты нативного инпута
     */
    type?: string;
    /**
     * Текущее введёное значение
     */
    modelValue?: string;
    /**
     * Даёт возможность отключить autocomplete при вводе
     */
    autocomplete?: boolean;
    /**
     * Дает возможность автозаполнения для конкретного типа (Пример: one-time-code)
     */
    autocompleteName?: AutocompleteNameType;
    /**
     * Лейбл инпута
     */
    label?: string;
    /**
     * Плейсхолдер инпута
     */
    placeholder?: string;
    /**
     * Сообщение пользователю, может использоваться для валидации
     */
    msg?: string;
    prefixIcon?: string;
    /**
     * Можно передать название иконки svg-sprite, для отображения в поле ввода
     */
    suffixIcon?: string;
    /**
     * Цвет иконки
     */
    suffixColor?: 'dark';
    /**
     * Параметр маски инпута, если необходим
     * @values phone, date, time, number, snils, inn, passport, payment, percent, year, pin, months
     */
    mask?: string;
    /**
     * Отображение маску при вводе
     */
    premask?: boolean;
    /**
     * Если активно, то при эмите, данные будут переданы с учётом активной маски.
     * Т.е. если в инпуте компонента +7 (999) 00-00-00, то без этого параметра,
     * будет передано 9990000. Включено по-умолчанию, для валидации
     */
    keepMasked?: boolean;
    /**
     * Ограничения на ввод только букв
     */
    lettersOnly?: boolean;
    /**
     * Модификатор вида с бордером
     */
    border?: boolean;
    /**
     * Наличие ошибки
     */
    error?: boolean;
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean;
    required?: boolean;
    readonly?: boolean;
    pointer?: boolean;
    info?: string;
    name?: string;
    infoRight?: string;
    arrowState?: boolean | null;
    /**
     * Определяет, является ли поле поиском
     */
    isSearch?: boolean;
    isClearBtn?: boolean;
    sizeClearBtn?: 'xSmall' | 'small' | 'medium' | 'large';
    /**
     * Результаты поиска
     */
    results?: SearchItem[] | null;
    fullWidth?: boolean;
    absoluteHint?: boolean;
    calendar?: boolean;
}

export interface InputThousandsProps {
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'medium'>,
    /**
     * Определяет классы, которые будут модифицировать тему
     */
    theme?: TTheme;
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>;
    /**
     * Текущее введёное значение
     */
    modelValue?: string;
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean;

    delimiter?: string;

    decimalMark?: string;

    decimalCount?: number;

    positiveOnly?: boolean;

    length?: { maxlength: number, minlength: number };
    name?: string;
}

export interface InputHintProps {
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    theme?: TTheme & 'alert';
    absolute?: boolean,
    disabled?: boolean,
}

export interface FileProps {
    label?: string,
    size?: Extract<TSize, 'medium'>,
    theme?: Extract<TTheme, 'light'>,
    placeholder?: string,
    mobilePlaceholder?: string,
    maxFilesCount?: number,
    maxFileSize?: number,
    maxSizeErrorText?: string,
    fileTypes?: Array<string>,
    fileTypeError?: string,
    serverError?: string,
    disabled?: boolean,
    required?: boolean,
    loading?: boolean,
    info?: string,
    name?: string,
    /**
     * Сообщение пользователю, может использоваться для валидации
     */
    msg?: string;
}

export interface TextAreaProps {
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'medium'>,
    /**
     * Определяет классы, которые будут модифицировать тему
     */
    theme?: Extract<TTheme, 'light'>,
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>,
    /**
     * Текущее введёное значение
     */
    modelValue?: string;
    /**
     * Даёт возможность отключить autocomplete при вводе
     */
    autocomplete?: boolean;
    /**
     * Лейбл инпута
     */
    label?: string;
    /**
     * Плейсхолдер инпута
     */
    placeholder?: string;
    /**
     * Сообщение пользователю, может использоваться для валидации
     */
    msg?: string;
    /**
     * Наличие ошибки
     */
    error?: boolean;
    /**
     * Это свойство отключает взаимодействие
     */
    disabled?: boolean;
    required?: boolean;
    name?: string;
}

export interface InputSearchResults {
    results?: SearchItem[] | null;
}

export interface InputOtpProps {
    /**
     * Определяет классы, которые будут модифицировать размер
     */
    size?: Extract<TSize, 'medium'>,
    /**
     * Определяет классы, которые будут модифицировать тему
     */
    theme?: TTheme;
    /**
     * Определяет классы, которые будут модифицировать цвет
     */
    color?: Extract<TColor, 'primary'>;
    /**
     * Это свойство отключает взаимодействие
     */
    /**
     * Лейбл инпута
     */
    label?: string;
    /**
     * Плейсхолдер инпута
     */
    placeholder?: string;
    /**
     * Сообщение пользователю, может использоваться для валидации
     */
    /**
     * Наличие ошибки
     */
    error?: boolean;
    msg?: string;
    disabled?: boolean;
    required?: boolean;
    name?: string;
}
