<script setup lang="ts">
import type { PropsCalendarPickerPopup } from '~/components/ui/calendar/types';

const {
    date,
    time,
    availableTime,
    disabledDates,
    todayTomorrowStatus,
    todayTomorrowFacets,
    theme = 'light',
    hasDate,
    hasTime,
    mobileModal,
} = defineProps<PropsCalendarPickerPopup>();

const emit = defineEmits<{
    'click-today': [value: MouseEvent],
    'click-tomorrow': [value: MouseEvent],
    'change-time': [value: string],
    'change-date': [value: string],
}>();

// #region Data
const $style = useCssModule();
// #endregion

const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style._mobileModal]: mobileModal,
    },
]);
</script>

<template>
    <div :class="[$style.VCalendarPickerPopup, classList]">
        <template v-if="hasDate">
            <div
                v-if="todayTomorrowFacets && todayTomorrowFacets.length"
                :class="$style.today"
            >
                <div
                    :class="[$style.btn, {[$style._active]: todayTomorrowStatus === 'today'}, {[$style._disabled]: !todayTomorrowFacets[0]}]"
                    @click="emit('click-today', $event)"
                >
                    Сегодня
                </div>
                <div
                    :class="[$style.btn, {[$style._active]: todayTomorrowStatus === 'tomorrow'}, {[$style._disabled]: !todayTomorrowFacets[1]}]"
                    @click="emit('click-tomorrow', $event)"
                >
                    Завтра
                </div>
            </div>
            <client-only>
                <VDatePicker
                    :model-value="date"
                    :class="['calendarPicker', {[`_${theme}`]: theme}, {[`_mobileModal`]: mobileModal}]"
                    borderless
                    :disabled-dates="disabledDates"
                    @update:model-value="emit('change-date', $event)"
                />
            </client-only>
        </template>
        <div
            v-if="hasTime && availableTime && availableTime.length"
            :class="[$style.time, {[$style._onlyTime]: !hasDate}]"
        >
            <VTimePicker
                :model-value="time"
                :available-time="availableTime"
                :disabled="hasDate && !date"
                :theme="theme"
                @update:model-value="emit('change-time', $event)"
            />
        </div>
    </div>
</template>

<style module lang="scss">
    .VCalendarPickerPopup {
        position: absolute;
        top: calc(100% + 1.2rem);
        left: 0;
        z-index: 100;
        min-width: 29rem;
        padding: 2rem;
        border-radius: 1.2rem;

        &._light {
            .btn {
                background-color: $base-100;
                color: $base-600;
                transition: $default-transition;

                &._active {
                    background-color: $base-600;
                    color: $base-0;

                    @include hover {
                        &:hover {
                            background-color: $base-600;
                            opacity: .8;
                        }
                    }
                }

                &._disabled {
                    background-color: $base-100;
                    color: $base-400;
                }

                @include hover {
                    &:hover {
                        background-color: $base-200;
                    }
                }
            }

            .time {
                border-color: $base-200;
            }
        }
    }

    .btn {
        display: inline-block;
        padding: .6rem 1.2rem;
        border-radius: .4rem;
        font-size: 1.2rem;
        cursor: pointer;
        user-select: none;

        &._disabled {
            pointer-events: none;
        }

        &:first-child {
            margin-right: .4rem;
        }
    }

    .today {
        position: absolute;
        top: 7.6rem;
        z-index: 1;
    }

    .time {
        &:not(._onlyTime) {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid;
        }
    }
</style>

<style lang="scss">
    .calendarPicker {
        margin-top: -.4rem;

        /* Colors */
        &._light {
            .vc-header {
                .vc-title {
                    color: $base-600;
                }

                .vc-arrow {
                    background-color: $base-100;

                    @include hover {
                        &:hover {
                            background-color: $base-200;
                        }
                    }
                }
            }

            .vc-weeks {
                .vc-weekday {
                    color: $base-500;
                }
            }

            .vc-day {
                &:not(.is-not-in-month) {
                    .vc-day-content {
                        background-color: $base-100;

                        @include hover {
                            &:hover {
                                background-color: $base-200;
                            }
                        }
                    }
                }

                .vc-day-content {
                    &.vc-disabled {
                        background-color: $base-0;
                        color: $base-400;
                    }

                    &.vc-highlight-content-solid {
                        background-color: $base-600;
                    }
                }

                &.is-not-in-month {
                    .vc-day-content {
                        color: $base-400;
                    }
                }

                .vc-highlight {
                    background-color: $base-600;
                }
            }
        }

        &._mobileModal {
            width: 100%;

            .vc-day {
                .vc-day-content {
                    @include respond-to(tablet) {
                        width: 6rem;
                    }

                    @include respond-to(mobile) {
                        width: 4.6rem;
                    }
                }
            }
        }

        .vc-header {
            margin-top: .4rem;
            margin-bottom: 7.2rem;
            padding: 0;
            font-family: $base-font;
            font-size: 1.4rem;

            .vc-title {
                padding: 0;
                text-transform: capitalize;
                font-weight: bold;
            }

            .vc-arrow {
                width: 3.2rem;
                height: 3.2rem;
                margin-top: .2rem;
                border-radius: 3.2rem;
                transition: $default-transition;

                & > svg {
                    width: 1.2rem;
                    height: 1.2rem;
                }
            }
        }

        .vc-title-wrapper {
            position: absolute;
            left: 0;
        }

        .vc-prev,
        .vc-next {
            position: absolute;
            right: 0;
        }

        .vc-prev {
            transform: translateX(calc(-100% - .4rem));
        }

        .vc-weeks {
            padding: 0;
            font-family: $base-font;

            .vc-weekdays {
                margin-bottom: .4rem;
            }

            .vc-weekday {
                font-size: 1.2rem;
            }
        }

        .vc-week {
            gap: .2rem;

            &:not(:last-child) {
                margin-bottom: .2rem;
            }
        }

        .vc-day {
            .vc-day-content {
                width: 3.4rem;
                height: 3.4rem;
                border-radius: .4rem;
                font-size: 1.2rem;

                &.vc-disabled {
                    pointer-events: none;
                }

                &.vc-highlight-content-solid {
                    pointer-events: none;
                }
            }

            &.is-not-in-month {
                pointer-events: none;

                .vc-day-content {
                    opacity: 1;
                }
            }

            .vc-highlight {
                pointer-events: none;
                width: 3.4rem;
                height: 3.4rem;
                border-radius: .4rem;
            }
        }

        .vc-focus:focus-within {
            outline: none;
            box-shadow: none;
        }
    }
</style>
