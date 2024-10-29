import type { TTheme } from '~/types/ui/type';

export interface VFilterModalProps {
    title?: string,
    btnText?: string,
    btnVisible?: boolean,
    resetVisible?: boolean,
    resetText?: string,
    innerModal?: boolean,
}

export interface VFilterContainerProps {
    label?: string,
    size?: string,
    hasMarginLeft?: boolean,
}

export interface VFilterPopoverProps {
    label?: string,
    active?: boolean,
    position?: string,
    /** Ширина контента поповера (при наличии скролящегося контента указание обязательно) */
    popWidth?: string,
    hasLeftActive?: boolean,
    hasRightActive?: boolean,
    hasLeftInteracting?: boolean,
    hasRightInteracting?: boolean,
    theme?: TTheme,
}
