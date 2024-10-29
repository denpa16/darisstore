import { defineComponent, h, withCtx } from 'vue';
import Component from './VCircleButton.vue';
import RawComponent from './VCircleButton.vue?raw';
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
    icon: { default: 'arrow-left', type: 'input' },
};

export default defineComponent({
    name: 'VCircleButtonDemo',
    components: { Component },

    setup(_, { slots }) {
        return () => h(Component, null, {
            default: withCtx(() => slots.default ? slots.default() : []),
        });
    },
});
