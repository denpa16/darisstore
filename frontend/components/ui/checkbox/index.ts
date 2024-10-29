import type { TTheme } from '~/types/ui/type';

export interface Props {
    name?: string;
    modelValue?: Array<string | boolean> | string | boolean;
    trueValue?: string | boolean;
    falseValue?: string | boolean;
    size?: 'medium' | 'pre-medium' | 'small';
    theme?: TTheme;
    radio?: boolean,
    coloredLabel?: boolean,
    disabled?: boolean,
    msg?: string,
    info?: string,
    label: string,
}
