import { defineComponent, h, withCtx } from 'vue';
import Component from './VButton.vue';
import RawComponent from './VButton.vue?raw';
import type { IStoryOptions } from '@idaproject/ui-kit/components/story/types.ts';

export const componentRaw = RawComponent;
export const category = 'Base';

export const values: Record<string, IStoryOptions> = {
    theme: {
        default: 'light',
        vars: ['light', 'dark'],
        type: 'tabs',
    },
    color: {
        default: 'primary',
        vars: ['primary', 'secondary', 'tertiary'],
        type: 'tabs',
    },
    size: {
        default: 'small',
        vars: ['small', 'medium', 'large'],
        type: 'tabs',
    },
    active: { default: false, type: 'boolean' },
    disabled: { default: false, type: 'boolean' },
    loading: { default: false, type: 'boolean' },
    slot: { default: 'Button', type: 'input' },
};

export default defineComponent({
    name: 'VButtonDemo',
    components: { Component },

    setup(_, { slots }) {
        return () => h(Component, null, {
            default: withCtx(() => slots.default ? slots.default() : []),
        });
    },
});
