import type { TSize, TTheme } from '@/types/ui/type.ts';

export type TIconSize = 'xs' | 'small' | 'sMedium' | 'medium' | 'sLarge' | 'large' | 'xxLarge' | 'custom'

export interface VIconProps {
    size?: Extract<TSize, 'medium' | 'small'>;
    name?: string
}

export interface VRubProps {
    symbol?: string;
}

export interface VLoadingProps {
    size?: Extract<TSize, 'medium' | 'small'>;
    theme?: TTheme
}
