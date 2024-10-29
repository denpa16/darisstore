import type { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils';

export type ChoiceValue = string | number | boolean | null | [];
export type ChoiceLabel = string | number;
export type ChoiceValueKeyType = 'value';
export type ChoiceLabelKeyType = 'label';

export interface Choice {
    [choiceValueKey]: ChoiceValue;
    [choiceLabelKey]?: ChoiceLabel;
    project_slug?: string;
    min_price?: number;
    time?: number | null;
    on_foot?: boolean;
    metro_color?: string;
    text?: string | null;
    image_display?: string | null;
}

export interface Range {
    min: number;
    max: number;
}

export interface RangeValue {
    min: number | null;
    max: number | null;
}

export type RangeCompletion = {
    min: string | null,
    max: string | null,
};

export interface ServerSpec {
    name: string;
    choices?: Choice[];
    ranges?: Range;
    range?: Range;
}

export type ClientSpecs = Record<ChoiceLabel, Choice[] | Range | RangeCompletion>
export type ClientFacets = Record<ChoiceLabel, ChoiceValue[] | Range | RangeCompletion>

export type FacetsType = Record<ChoiceLabel, ChoiceValue[] | Range | RangeCompletion | undefined | null>
