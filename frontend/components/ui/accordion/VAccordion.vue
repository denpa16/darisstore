<script setup lang="ts">
/**
 * Позволяет пользователям отображать и скрывать разделы связанного контента на странице.
 *
 * @version 1.0.1
 * @displayName VAccordion
 */

// #region Imports
import type VAccordionItem from '~/components/ui/accordion/VAccordionItem.vue';
// #endregion

// #region Props
export interface IProps {
    multiple?: boolean;
    name?: string;
}

const {
    multiple = false,
    name = '',
} = defineProps<IProps>();
// #endregion

// #region Data
// eslint-disable-next-line no-extra-parens
const panels = ref<(InstanceType<typeof VAccordionItem> | null)[]>([]);
// eslint-disable-next-line no-extra-parens
const open = ref<(InstanceType<typeof VAccordionItem> | null)>(null);
// #endregion

// #region Lifecycle
provide('vAccordionRegister', register);
provide('vAccordionUnregister', unregister);
provide('vAccordionSetOpen', setOpen);
// #endregion

// #region Methods
function register(panel: InstanceType<typeof VAccordionItem>) {
    panels.value.push(panel);
}

function unregister(panel: InstanceType<typeof VAccordionItem>) {
    if (!multiple && open.value === panel) {
        open.value = null;
    }

    const index = panels.value.findIndex(p => p.uid === panel.uid);
    panels.value.splice(index, 1);
}

function setOpen(panel: InstanceType<typeof VAccordionItem>, isOpen: boolean) {
    if (!multiple) {
        for (let i = 0; i < panels.value.length; i++) {
            const item = panels.value[i];
            if (isOpen && item.uid !== panel.uid) {
                item.exposed.toggle(false);
            }
        }

        if (!isOpen) {
            open.value = null;
        } else {
            open.value = panel;
        }
    }
}

// #endregion
</script>

<template>
    <div
        :class="$style.VAccordion"
        :data-test-id="name"
    >
        <!-- @slot Список компонентов VAccordionItem -->
        <slot></slot>
    </div>
</template>

<style lang="scss" module>
    .VAccordion {
        position: relative;
        z-index: 1;
    }
</style>
