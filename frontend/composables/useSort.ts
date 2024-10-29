import { choiceLabelKey, choiceValueKey } from '@/assets/ts/utils/filter-utils';
import type { ChoiceLabel, ChoiceValue, RangeValue } from '~/types/filter';

export function useSort(values: Record<ChoiceLabel, ChoiceValue | ChoiceValue[] | RangeValue>) {
    // #region Data
    const sortList = [
        { [choiceLabelKey]: 'По умолчанию', [choiceValueKey]: null },
        { [choiceLabelKey]: 'По возрастанию цены', [choiceValueKey]: 'price,pk,mode' },
        { [choiceLabelKey]: 'По убыванию цены', [choiceValueKey]: '-price,pk,mode' },
        { [choiceLabelKey]: 'По возрастанию площади', [choiceValueKey]: 'area,pk,mode' },
        { [choiceLabelKey]: 'По убыванию площади', [choiceValueKey]: '-area,pk,mode' },
        { [choiceLabelKey]: 'По возрастанию скидки', [choiceValueKey]: 'discount,pk,mode' },
        { [choiceLabelKey]: 'По убыванию скидки', [choiceValueKey]: '-discount,pk,mode' },
    ];
    // #endregion

    // #region Computed
    const iconSort = computed(() => {
        if (values.ordering && typeof values.ordering === 'string') {
            return values.ordering[0] === '-' ? 'sort-desc' : 'sort-asc';
        }

        return 'arrow-up-down';
    });
    // #endregion

    return {
        sortList,
        iconSort,
    };
}
