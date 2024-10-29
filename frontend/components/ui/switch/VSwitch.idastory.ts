import { defineComponent, h } from 'vue';
import Component from './VSwitch.vue';

import RawComponent from './VSwitch.vue?raw';
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
    disabled: { default: false, type: 'boolean' },
    modelValue: { default: false, newValue: true, type: 'interaction' },
};

export default defineComponent({
    name: 'VSwitchDemo',
    components: { Component },

    setup(_) {
        return () => h(Component, null, {
            default: () => [],
        });
    },
});
