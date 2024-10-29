import type { Range } from '~/types/filter';
import type { TColor, TSize, TTheme } from '@/types/ui/type.ts';

export interface VRangeProps {
    name?: string;
    size?: Extract<TSize, 'small' | 'medium'>;
    theme?: Extract<TTheme, 'light'>;
    color?: Extract<TColor, 'primary'>;
    label?: string;
    postfix?: string;
    prefixes?: Array<string>;
    bottomLabels?: Array<string>;
    specs: Range;
    facets?: Range;
    step?: number;
    valueMin?: number | null;
    valueMax?: number | null;
    single?: boolean;
    positiveOnly?: boolean;
    disabled?: boolean;
    showPercent?: boolean,
    valueFilter?: (val: string) => string,
    valueParser?: (val: string) => string,
    dynamicInputWidth?: boolean,
    decimalCount?: number;
    decimalMark?: string;
}

export interface VRangeSliderProps {
    min?: number;
    max?: number;
    step?: number;
    modelValue?: number | number[];
    range?: boolean;
    vertical?: boolean;
    height?: string;
    disabled?: boolean;
    showStops?: boolean;
    showValue?: boolean;
    valueFormat?: (val: string | number | null) => string;
    marks?: Record<number | string, unknown>;
    noTransition?: boolean;
    theme?: Extract<TTheme, 'light'>;
    color?: Extract<TColor, 'primary'>;
}

export interface VRangeSliderDotProps {
    modelValue?: number;
    vertical?: boolean;
    dragging?: boolean;
    sliderSize: number,
    precision: number,
    min: number;
    max: number;
    step: number;
    disabled: boolean,
}
