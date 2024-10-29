import type { TTheme } from '@/types/ui/type.ts';

export interface VScrollBoxProps {
    width?: string,
    height?: string,
    resizable?: boolean,
    skipOffset?: boolean,
    hasMargin?: boolean,
    fade?: boolean,
    theme?: TTheme
}
