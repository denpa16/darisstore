import { defineComponent, h } from 'vue';
import Component from './VInputOtp.vue';

import RawComponent from './VInputOtp.vue?raw';
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
    error: { default: false, type: 'boolean' },
    placeholder: { default: '0' },
    label: { default: 'Label', type: 'input' },
    msg: { default: 'msg' },
};

export default defineComponent({
    name: 'VInputOtpDemo',
    components: { Component },

    setup(_) {
        return () => h(Component, null, {
            default: () => [],
        });
    },
});
