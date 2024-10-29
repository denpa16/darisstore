<script setup lang="ts">

// #region Imports
// Vue
import { onClickOutside } from '@vueuse/core';

// Types
import type { Props } from './types.ts';
import { ColorsEnum, ThemeEnum } from '@/types/ui/type.ts';
// #endregion

// #region Props
const {
    attach = '#app',
    attachRelative = false,
    top = false,
    bottom = false,
    left = false,
    right = false,
    rightToActivator = false,
    hoverable = false,
    isPopover = false,
    disabled = false,
    nudge = 8,
    offsetY = 12,
    offsetX = 12,
    text = '',
    color = ColorsEnum.primary,
    theme = ThemeEnum.light,
    tag = 'div',
} = defineProps<Props>();
// #endregion

// #region Emits
const emit = defineEmits(['enter', 'blur', 'click']);
// #endregion

// #region Data
const $style = useCssModule();
const slots = useSlots();
const isVisible = ref(false);
const isDetached = ref(false);
const dimensions = reactive({
    activator: { top: 0, left: 0, width: 0, height: 0 },
    content: { top: 0, left: 0, width: 0, height: 0 },
    page: { top: 0, left: 0, width: 0, height: 0 },
    attach: { top: 0, left: 0, width: 0, height: 0 },
});
const target = ref<HTMLElement | null>(null);
const timeout = ref<number | null>(null);
const clickTimeout = ref<number | null>(null);
const activatorRef = ref<HTMLElement | null>(null);
const contentRef = ref<HTMLElement | null>(null);
// #endregion

// #region Computed
const contentClasses = computed(() => [
    {
        [$style._top]: top || !bottom && !left && !top && !right,
        [$style._bottom]: bottom,
        [$style._left]: left,
        [$style._right]: right,
        [$style._disabled]: disabled,
        [$style[`_${color}`]]: color,
        [$style[`_${theme}`]]: theme,
        [$style._hoverable]: hoverable,
    },
]);


const contentStyles = computed(() => {
    if (attach && attachRelative) {
        return {
            top: !bottom ? typeof offsetY === 'number' ? `${offsetY}px` : offsetY : null,
            left: !right ? typeof offsetX === 'number' ? `${offsetX}px` : offsetX : null,
            right: right ? typeof offsetX === 'number' ? `${offsetX}px` : offsetX : null,
            bottom: bottom ? typeof offsetY === 'number' ? `${offsetY}px` : offsetY : null,
        };
    }

    const { activator, content } = dimensions;
    const unknown = !bottom && !left && !top && !right;
    let newTop = 0;
    let newLeft = 0;

    if (top || bottom || unknown) {
        newTop = activator.top + (bottom ? activator.height : -content.height) + (bottom ? nudge : -nudge);
        newLeft = activator.left + activator.width / 2 - content.width / 2;

        if (rightToActivator) {
            newLeft = activator.left + activator.width - content.width;
        }
    } else if (left || right) {
        newTop = activator.top + activator.height / 2 - content.height / 2;
        newLeft = activator.left + (right ? activator.width : -content.width) + (right ? nudge : -nudge);
    }

    const topWOverflow = calcYOverflow(newTop);
    const leftWOverflow = calcXOverflow(newLeft);

    return {
        top: `${attach ? topWOverflow - dimensions.attach.top : topWOverflow}px`,
        left: `${attach ? leftWOverflow - dimensions.attach.left : leftWOverflow}px`,
        '--x-shift': `${newLeft - leftWOverflow}px`,
        '--y-shift': `${newTop - topWOverflow}px`,
        '--triangle-display': (left || right) && newLeft !== leftWOverflow ? 'none' : 'block',
    };
});
// #endregion

// #region Lifecycle
onClickOutside(activatorRef, () => hide());

onMounted(() => {
    if (!slots.activator) {
        console.error('[VTooltip] activator slot must be bound');
    }
});

// Before destroy
onBeforeUnmount(() => {
    if (isDetached.value && target.value) {
        target.value.removeChild(contentRef.value as HTMLElement);
    }
});
// #endregion

// #region Methods
async function handleInit() {
    if (!isDetached.value) {
        initDetach();
    }

    if (timeout.value && isVisible.value) {
        clearTimeout(timeout.value);
        timeout.value = null;
    } else {
        emit('enter');
        isVisible.value = true;
        await nextTick();
        updateDimensions();
    }
}

function onActivatorEnter() {
    if (isPopover) {
        return;
    }

    handleInit();
}

function onActivatorClick() {
    if (disabled) {
        return;
    }

    if (isVisible.value) {
        if (!isPopover) {
            onActivatorLeave();
        } else {
            hide();
        }
    } else {
        handleInit();
        clickTimeout.value = window.setTimeout(onActivatorLeave, 5000);
    }
}

function onActivatorLeave() {
    if (isPopover) {
        return;
    }

    hide();
}

function onContentEnter() {
    if (!hoverable) {
        return;
    }

    clearTimeout(timeout.value as number);
    timeout.value = null;
}

function onContentLeave() {
    if (!hoverable) {
        return;
    }

    hide();
}

function hide() {
    timeout.value = window.setTimeout(() => {
        isVisible.value = false;
        clearTimeout(timeout.value as number);
        clearTimeout(clickTimeout.value as number);
        timeout.value = null;
        clickTimeout.value = null;
        emit('blur');
    }, 50);
}

function updateDimensions() {
    if (activatorRef.value) {
        const activatorBounding = activatorRef.value.getBoundingClientRect();
        dimensions.activator.top = activatorBounding.top + window.scrollY;
        dimensions.activator.left = activatorBounding.left + window.scrollX;
        dimensions.activator.width = activatorBounding.width;
        dimensions.activator.height = activatorBounding.height;
    } else {
        console.warn('[CTooltip] updateDimensions error - activator is undefined');
    }

    if (contentRef.value) {
        const contentBounding = contentRef.value.getBoundingClientRect();
        dimensions.content.top = contentBounding.top + window.scrollY;
        dimensions.content.left = contentBounding.left + window.scrollX;
        dimensions.content.width = contentBounding.width;
        dimensions.content.height = contentBounding.height;
    } else {
        console.warn('[CTooltip] updateDimensions error - content is undefined');
    }

    dimensions.page.width = document.documentElement.clientWidth || window.innerWidth;
    dimensions.page.height = document.documentElement.clientHeight || window.innerHeight;
    dimensions.page.top = window.scrollY || document.documentElement.scrollTop;
    dimensions.page.left = window.scrollX || document.documentElement.scrollLeft;

    if (attach) {
        const attachEl = document.querySelector(attach);
        if (attachEl) {
            const attachBounding = attachEl.getBoundingClientRect();
            dimensions.attach.top = attachBounding.top + window.scrollY;
            dimensions.attach.left = attachBounding.left + window.scrollX;
            dimensions.attach.width = attachBounding.width;
            dimensions.attach.height = attachBounding.height;
        }
    }
}

function calcYOverflow(top: number) {
    const topOverflow = dimensions.page.top + offsetY - top;
    const bottomOverflow = top + dimensions.content.height + offsetY - (dimensions.page.top + dimensions.page.height);

    let attachTopOverflow = 0;
    let attachBottomOverflow = 0;

    if (attach) {
        attachTopOverflow = dimensions.attach.top + offsetY - top;
        attachBottomOverflow = top + dimensions.content.height + offsetY - (dimensions.attach.top + dimensions.attach.height);
    }

    if (topOverflow > 0) {
        top = dimensions.page.top + offsetY;
    } else if (attach && attachTopOverflow > 0) {
        top = dimensions.attach.top + offsetY;
    } else if (bottomOverflow > 0) {
        top = dimensions.page.top + dimensions.page.height - offsetY - dimensions.content.height;
    } else if (attach && attachBottomOverflow > 0) {
        top = dimensions.attach.top + dimensions.attach.height - offsetY - dimensions.content.height;
    }

    return top;
}

function calcXOverflow(left: number) {
    const leftOverflow = dimensions.page.left + offsetX - left;
    const rightOverflow = left + dimensions.content.width + offsetX - (dimensions.page.left + dimensions.page.width);

    let attachLeftOverflow = 0;
    let attachRightOverflow = 0;

    if (attach) {
        attachLeftOverflow = dimensions.attach.left + offsetY - left;
        attachRightOverflow = left + dimensions.content.width + offsetY - (dimensions.attach.left + dimensions.attach.width);
    }

    if (attach && attachLeftOverflow > 0) {
        left = dimensions.attach.left + offsetY;
    } else if (leftOverflow > 0) {
        left = dimensions.page.left + offsetX;
    } else if (attach && attachRightOverflow > 0) {
        left = dimensions.attach.left + dimensions.attach.width - offsetY - dimensions.content.width;
    } else if (rightOverflow > 0) {
        left = dimensions.page.left + dimensions.page.width - offsetX - dimensions.content.width;
    }

    return left;
}

function initDetach() {
    target.value = document.querySelector(attach);

    if (!target.value) {
        console.warn(`[CTooltip] Unable to locate target ${attach}`);
        return;
    }

    try {
        target.value.appendChild(contentRef.value as HTMLElement);
    } catch (e) {
        console.log(e);
    }

    isDetached.value = true;
}

// #endregion
</script>

<template>
    <component
        :is="tag"
        ref="activatorRef"
        :class="$style.VTooltip"
        @mouseenter="onActivatorEnter"
        @mouseleave="onActivatorLeave"
        @click.stop="onActivatorClick"
    >

        <slot name="activator"></slot>

        <div
            ref="contentRef"
            :class="[$style.content, ...contentClasses]"
            :style="contentStyles"
            @mouseenter="onContentEnter"
            @mouseleave="onContentLeave"
        >
            <transition name="tooltip">
                <div v-if="isVisible">
                    <slot name="content">
                        <div :class="$style.contentDefault">
                            <slot>
                                <div :class="$style.contentDefaultText" v-html="text"></div>
                            </slot>
                        </div>
                    </slot>
                </div>
            </transition>
        </div>
    </component>
</template>

<style lang="scss" module>
    .VTooltip {
        position: relative;
        display: flex;
        cursor: pointer;
    }

    .content {
        --x-shift: 0;
        --y-shift: 0;
        --triangle-display: "block";

        position: absolute;
        z-index: 200;
        pointer-events: none;

        @include respond-to(tablet) {
            z-index: 110;
        }

        /* Themes */
        &._light {
            &._primary {
                .contentDefault {
                    background-color: $base-0;
                    color: $base-600;
                    box-shadow: 0 4px 38px 0 rgb(0 0 0 / 8%);

                    &:after {
                        background-color: $base-0;
                    }
                }
            }
        }

        &._dark {
            &._primary {
                .contentDefault {
                    background-color: $base-800;
                    color: $base-400;
                    box-shadow: 0 4px 38px 0 rgb(0 0 0 / 8%);

                    &:after {
                        background-color: $base-800;
                    }
                }
            }
        }

        /** End Themes */

        &._hoverable {
            pointer-events: all;
        }

        &._bottom {
            .contentDefault {
                &:after {
                    top: 0;
                    bottom: auto;
                    left: 50%;
                    transform: rotate(45deg) translate(-60%, 0);
                }
            }
        }

        &._left {
            .contentDefault {
                &:after {
                    top: 50%;
                    bottom: auto;
                    left: 100%;
                    transform: rotate(45deg) translate(-60%, 0);
                }
            }
        }

        &._right {
            .contentDefault {
                &:after {
                    top: 50%;
                    bottom: auto;
                    left: 0;
                    transform: rotate(45deg) translate(-60%, 0);
                }
            }
        }
    }

    .contentDefault {
        @include text(l3m);

        position: relative;
        padding: 1.2rem;

        &:after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            display: block;
            width: 1.2rem;
            height: 1.2rem;
            transform: rotate(45deg) translate(-60%, 0);
        }
    }
</style>
