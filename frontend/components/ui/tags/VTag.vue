<script setup lang="ts">
// #region Imports
// Vue
import { resolveComponent } from 'vue';
// Types
import type { VTagProps } from './types.ts';
// #endregion

// #region Props
const {
    to,
    href,
    size = 'small',
    iconBefore,
    iconAfter,
    iconSize = 'small',
    info,
    color,
    label = 'Label',
    tag = 'span',
    isChips = false,
    disabled = false,
} = defineProps<VTagProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    close: [],
}>();
// #endregion

// #region Data
const isClosed = ref<boolean>(false);
const $style = useCssModule();
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${color}`]]: color,
        [$style[`_${size}`]]: size,
        [$style._chips]: isChips,
        [$style._disabled]: disabled,
    },
]);

const linkComponent = computed(() => {
    const isLink = !disabled && to;
    if (!isLink) {
        return {
            is: tag,
        };
    }

    return {
        is: resolveComponent('NuxtLink'),
        to,
    };
});
// #endregion

// #region Methods
function close() {
    if (!isChips) {
        return;
    }

    isClosed.value = true;
    emit('close');
}
//
</script>

<template>
    <Transition name="fade">
        <component
            :is="linkComponent.is"
            v-if="!isClosed"
            :to="linkComponent.to"
            :class="[$style.VTag, classList]"
            :href="tag === 'a' ? href : undefined"
            v-bind="$attrs"
        >
            <slot name="iconBefore">
                <VIcon
                    v-if="iconBefore"
                    :name="iconBefore"
                    :size="iconSize"
                    :class="$style.iconBefore"
                />
            </slot>

            <slot><span :class="$style.label">{{ label }}</span></slot>

            <slot name="iconAfter">
                <template v-if="info">
                    <VTooltip text="Текст тултипа">
                        <template #activator>
                            <VIcon
                                name="mock-information"
                                :size="iconSize"
                                :class="$style.iconAfter"
                            />
                        </template>
                    </VTooltip>
                </template>
                <template v-else>
                    <VIcon
                        v-if="iconAfter"
                        :name="iconAfter"
                        :size="iconSize"
                        :class="$style.iconAfter"
                        @click="close"
                    />
                </template>
            </slot>
        </component>
    </Transition>
</template>

<style lang="scss" module>
    .VTag {
        display: inline-grid;
        grid-auto-flow: column;
        align-items: center;
        gap: .4rem;
        user-select: none;
        width: fit-content;
        border-radius: .4rem;
        border: .1rem solid;
        transition: $default-transition;

        @include text(l4-regular);

        /* -- Size -- */
        &._small {
            @include text(l5-regular);

            height: 2.4rem;
            padding: 0 .8rem;
        }

        &._medium {
            height: 3rem;
            padding: 0 1.2rem;
        }

        &._large {
            height: 3.2rem;
            padding: .7rem 1.2rem;
        }

        /* -- Color -- */
        &._default {
            border-color: $primary-100;
            color: $primary-100;

            .iconBefore {
                color: $primary-100;
            }

            .iconAfter {
                color: $primary-100;
            }
        }

        &._grey {
            border-color: rgba($base-600, 0);
            background-color: $base-100;
            color: $base-600;

            .iconBefore {
                color: $base-600;
            }

            .iconAfter {
                color: $base-400;
            }
        }

        &._green {
            border-color: rgba($base-0, 0);
            background-color: $additional-success-500;
            color: $base-0;

            .iconBefore {
                color: $base-0;
            }

            .iconAfter {
                color: $opacity-white-40;
            }
        }

        &._red {
            border-color: rgba($primary-600, 0);
            background-color: $primary-600;
            color: $primary-600;

            .iconBefore {
                color: $primary-600;
            }

            .iconAfter {
                color: rgba($primary-600, .4);
            }
        }

        &._grey-stroke {
            border-color: $base-400;
            color: $base-600;

            .iconBefore {
                color: $base-600;
            }

            .iconAfter {
                color: $base-400;
            }
        }

        &._green-stroke {
            border-color: $additional-success-500;
            color: $additional-success-500;

            .iconBefore {
                color: $additional-success-500;
            }

            .iconAfter {
                color: rgba($additional-success-500, .4);
            }
        }

        &._red-stroke {
            border-color: $primary-600;
            color: $primary-600;

            .iconBefore {
                color: $primary-600;
            }

            .iconAfter {
                color: rgba($primary-600, .4);
            }
        }

        &._premium-stroke {
            border-color: $premium-600-main;
            color: $premium-600-main;

            .iconBefore,
            .iconAfter {
                color: $premium-600-main;
            }
        }

        &._grey-fill {
            border-color: transparent;
            background-color: rgba($base-0, .1);
            color: $base-0;

            .iconBefore,
            .iconAfter {
                color: $base-0;
            }
        }

        &._red-light-fill {
            border-color: transparent;
            background-color: $primary-600;
            color: $primary-600;

            .iconBefore,
            .iconAfter {
                color: $primary-600;
            }
        }

        &._pink {
            border-color: transparent;
            background-color: $primary-600;
            color: $primary-600;

            .iconBefore,
            .iconAfter {
                color: $base-0;
            }
        }

        &._white {
            border-color: transparent;
            background-color: $base-0;
            color: $base-600;

            .iconBefore,
            .iconAfter {
                color: $base-600;
            }
        }

        &._blue {
            border-color: transparent;
            background-color: $primary-100;
            color: $base-0;

            .iconBefore,
            .iconAfter {
                color: $base-0;
            }
        }

        &._premium {
            border-color: transparent;
            color: $base-0;

            .iconBefore,
            .iconAfter {
                color: $base-0;
            }
        }

        /* -- Chips -- */
        &._chips {
            &._grey-stroke {
                border-color: $base-400;
                color: $base-600;

                .iconAfter {
                    color: $base-400;
                    opacity: 1;
                    cursor: pointer;
                }

                @include hover {
                    border-color: $base-600;
                }
            }

            &._disabled {
                cursor: not-allowed;

                &._grey-stroke {
                    border-color: $base-400;
                    color: $base-400;

                    .iconAfter {
                        color: $base-400;
                        pointer-events: none;
                    }
                }
            }
        }

        /* -- Border color -- */
        &._deepLight {
            border-color: $main-deep-light;
        }

        /* -- Chips -- */
    }

    .label {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .iconAfter,
    .iconBefore {
        transition: $default-transition;
    }

    .iconAfter {
        cursor: pointer;

        @include hover {
            opacity: .5;
        }
    }

</style>
