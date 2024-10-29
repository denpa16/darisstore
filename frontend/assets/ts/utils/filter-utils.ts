import type {
    ChoiceLabelKeyType,
    ChoiceValueKeyType,
    ClientSpecs,
    ServerSpec,
} from '~/types/filter';

export const choiceValueKey: ChoiceValueKeyType = 'value';
export const choiceLabelKey: ChoiceLabelKeyType = 'label';

export const prepareSpecs = (arr: ServerSpec[]) => {
    if (!Array.isArray(arr)) {
        console.warn('[prepareSpecs] Specs response is not an Array! Got ' + arr);
        return {};
    }

    const specs: ClientSpecs = {};
    arr.forEach(spec => {
        specs[spec.name] = spec.choices || spec.ranges || spec.range || { min: 0, max: 0 };
    });
    return specs;
};
