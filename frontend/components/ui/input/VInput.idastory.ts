import { defineComponent, h } from 'vue';
import Component from './VInput.vue';

import RawComponent from './VInput.vue?raw';
import type { IStoryOptions } from '@idaproject/ui-kit/components/story/types.ts';

export const componentRaw = RawComponent;

export const category = 'Base';

export const values: Record<string, IStoryOptions> = {
    theme: {
        default: 'light',
        vars: ['light', 'dark'],
        type: 'tabs',
    },
    size: {
        default: 'medium',
        vars: ['medium'],
        type: 'switch',
    },
    disabled: { default: false, type: 'boolean' },
    required: { default: false, type: 'boolean' },
    pointer: { default: false, type: 'boolean' },
    error: { default: false, type: 'boolean' },
    modelValue: { default: '', type: 'input' },
    placeholder: { default: 'placeholder', type: 'input' },
    label: { default: 'Label', type: 'input' },
    msg: { default: 'msg' },
    prefixIcon: { default: 'file' },
    info: { default: '' },
    infoRight: { default: 'infoRight' },
};

export default defineComponent({
    name: 'VInputDemo',
    components: { Component },

    setup(_) {
        return () => h(Component, null, {
            default: () => [],
        });
    },
});
