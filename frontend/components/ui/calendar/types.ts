import type { TTheme } from '~/types/ui/type';
import type { Spec } from '~/types/models';

export interface PropsCalendarPicker {
    modelValue?: string;
    disabled?: boolean,
    hasDate?: boolean,
    hasTime?: boolean,
    msg?: string,
    info?: string,
    label?: string,
    placeholder?: string,
    availableTime?: Spec[],
    disabledDates: object[],
    error?: boolean,
    theme?: TTheme,
    alignLeft?: boolean,
    mobileModal?: boolean,
    required?: boolean,
    name?: string,
}

export interface PropsTimePicker {
    modelValue?: string;
    label?: string,
    availableTime: Spec[],
    disabled?: boolean,
    theme?: TTheme,
}

export interface PropsCalendarPickerPopup {
    date?: Date | null,
    time?: string | null,
    availableTime?: Spec[],
    disabledDates: object[],
    hasDate?: boolean,
    hasTime?: boolean,
    theme?: TTheme,
    todayTomorrowStatus: 'today'| 'tomorrow' | '',
    todayTomorrowFacets: boolean[],
    mobileModal?: boolean,
}

export interface CalendarPickerDisabledDates {
    start: number,
    end: number
}
