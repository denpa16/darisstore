<script setup lang="ts">
// #region Imports

import useCalendarPopupVisibility
    from '@idaproject/core/composables/ui/calendar/useCalendarPopupVisibility';
import useCalendarDateUpdate from '@idaproject/core/composables/ui/calendar/useCalendarDateUpdate';
import useCalendarTodayTomorrow
    from '@idaproject/core/composables/ui/calendar/useCalendarTodayTomorrow';
import type { PropsCalendarPicker } from './types'; // #endregion

// #endregion

// #region Props
const {
    info,
    label,
    placeholder,
    modelValue,
    availableTime,
    hasDate = true,
    hasTime,
    disabledDates,
    disabled,
    error,
    msg,
    theme = 'light',
    alignLeft,
    mobileModal = true,
    required,
    name = '',
} = defineProps<PropsCalendarPicker>();
// #endregion

const emit = defineEmits<{
    'update:modelValue': [value: string],
}>();

const $style = useCssModule();
const { picker, isPopupVisible } = useCalendarPopupVisibility();
const { date, time, dateString, setTodayTomorrowDate } = useCalendarDateUpdate(emit, toRef(() => modelValue), hasDate, hasTime);
const { todayTomorrowStatus, todayTomorrowFacets } = useCalendarTodayTomorrow(toRef(() => modelValue), date, picker, disabled);

// #region Computed
const classList = computed(() => [
    {
        [$style._disabled]: disabled,
        [$style._error]: error,
        [$style._left]: alignLeft,
        [$style[`_${theme}`]]: theme,
        [$style._mobileModal]: mobileModal,
    },
]);
const toggleMsg = computed(() => !isPopupVisible.value ? msg : '');

const mask = computed(() => {
    if (hasDate && hasTime) {
        return 'dateTime';
    }
    if (hasDate && !hasTime) {
        return 'date';
    }
    if (hasTime && !hasDate) {
        return 'time';
    }

    return null;
});

// #endregion

function handleChangeDate(value) {
    date.value = value;
    if (!availableTime?.find(item => item.value === time.value)) {
        time.value = '';
    }
}

function handleChangeTime(value: string) {
    time.value = value;
    isPopupVisible.value = false;
}
</script>

<template>
    <div
        ref="picker"
        :class="[$style.VCalendarPicker, classList]"
    >
        <div :class="$style.input">
            <VInput
                :label="label"
                suffix-icon="calendar"
                suffix-color="dark"
                :info="info"
                :mask="mask"
                :premask="false"
                :placeholder="placeholder"
                :model-value="dateString"
                :disabled="disabled"
                :error="error"
                :msg="toggleMsg"
                :theme="theme"
                :name="name"
                readonly
                absolute-hint
                pointer
                calendar
                :required="required"
                @input-click="isPopupVisible = !isPopupVisible"
            />
        </div>

        <transition name="fade-fast">
            <VCalendarPickerPopup
                v-show="isPopupVisible"
                :class="$style.popup"
                :theme="theme"
                :date="date"
                :time="time"
                :available-time="availableTime"
                :disabled-dates="disabledDates"
                :today-tomorrow-facets="todayTomorrowFacets"
                :today-tomorrow-status="todayTomorrowStatus"
                :has-date="hasDate"
                :has-time="hasTime"
                @change-date="handleChangeDate"
                @change-time="handleChangeTime"
                @click-today="setTodayTomorrowDate(true)"
                @click-tomorrow="setTodayTomorrowDate(false)"
            />
        </transition>

        <div
            v-if="mobileModal"
            :class="$style.mobileModal"
        >
            <transition
                name="fade-fast"
            >
                <VFilterModal
                    v-show="isPopupVisible"
                    :title="label"
                    :btn-visible="false"
                    @back="isPopupVisible = false"
                >
                    <VCalendarPickerPopup
                        :class="$style.popup"
                        :mobile-modal="mobileModal"
                        :theme="theme"
                        :date="date"
                        :time="time"
                        :available-time="availableTime"
                        :disabled-dates="disabledDates"
                        :today-tomorrow-facets="todayTomorrowFacets"
                        :today-tomorrow-status="todayTomorrowStatus"
                        :has-date="hasDate"
                        :has-time="hasTime"
                        @change-date="handleChangeDate"
                        @change-time="handleChangeTime"
                        @click-today="setTodayTomorrowDate(true)"
                        @click-tomorrow="setTodayTomorrowDate(false)"
                    />

                    <VButton
                        round
                        border
                        :class="$style.btn"
                        @click="isPopupVisible = !isPopupVisible"
                    >
                        Применить
                    </VButton>
                </VFilterModal>
            </transition>
        </div>
    </div>
</template>

<style module lang="scss">
    .VCalendarPicker {
        position: relative;

        /* Colors */
        &._light {
            .popup {
                background-color: $base-0;
                box-shadow: 0 4px 38px 0 rgb(0 0 0 / 8%);
            }
        }

        /* Mods */
        &._disabled {
            cursor: not-allowed;
        }

        &._left {
            .popup {
                right: 0;
                left: auto;
            }
        }

        &._mobileModal {
            .popup {
                @include respond-to(tablet) {
                    display: none;
                }
            }

            .mobileModal {
                display: none;

                @include respond-to(tablet) {
                    display: block;
                }

                .popup {
                    @include respond-to(tablet) {
                        top: 6.6rem;
                        left: 0;
                        display: block;
                        box-shadow: none;
                    }
                }
            }
        }
    }

    .btn {
        margin: auto 2rem 2rem;
    }
</style>
