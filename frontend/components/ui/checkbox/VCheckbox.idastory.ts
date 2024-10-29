import { defineComponent, h, withCtx } from 'vue';
import Component from './VCheckbox.vue';
import RawComponent from './VCheckbox.vue?raw';
import type { IStoryOptions } from '@idaproject/ui-kit/components/story/types.ts';

export const componentRaw = RawComponent;
export const category = 'Base';

export const values: Record<string, IStoryOptions> = {
    theme: {
        default: 'light',
        vars: ['light'],
    },
    size: {
        default: 'medium',
        vars: ['medium'],
    },
    radio: { default: false, type: 'boolean' },
    disabled: { default: false, type: 'boolean' },
    label: { default: 'Label', type: 'input' },
    slot: { default: 'slot', type: 'input' },
    info: { default: 'info', type: 'input' },
    modelValue: { default: false, newValue: true, type: 'interaction' },
};

export default defineComponent({
    name: 'VCheckboxDemo',
    components: { Component },


    setup(_, { slots }) {
        return () => h(Component, null, {
            default: withCtx(() => slots.default ? slots.default() : []),
        });
    },
});
