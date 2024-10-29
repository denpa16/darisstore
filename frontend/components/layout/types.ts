import type { Component } from 'vue';
import type { TTheme } from '~/types/ui/type';

export interface IHeader {
    theme?: TTheme;
}

export interface IMenu {
    theme?: TTheme;
}

export interface IModalStorage {
    key: string;
    openedVal: string;
    closedVal: string;
}

export interface IModalOptions {
    transition?: string;
    // Для работы с localStorage
    storage?: IModalStorage;
    // Для более гибкого функционала принимается произвольная функция
    /* eslint-disable-next-line */
    onClose?: Function;
}

// Для более гибкого функционала принимаются произвольные параметры

export type TModalAttrs = Record<any, any>

export interface IModalOpenEvent {
    component: Component;
    attrs?: TModalAttrs;
    options?: IModalOptions;
}

export interface IModalType {
    open: (component: Component, attrs?: TModalAttrs, options?: IModalOptions) => void;
    update: (attrs?: TModalAttrs) => void;
    close: () => void;
    /* eslint-disable */
    $on: Function;
    $emit: Function;
    $off: Function;
    /* eslint-enable */
}

export interface IModalState {
    attrs: TModalAttrs | null | undefined;
    // Для более гибкого функционала принимается произвольная функция
    /* eslint-disable-next-line */
    onClose: Function | null | undefined;
    key: number | string | undefined;
    transition: string;
    storage?: IModalStorage;
    isPopover?: boolean,
}
