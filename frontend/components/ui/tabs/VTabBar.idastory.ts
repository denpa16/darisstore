import { defineComponent, h } from 'vue';
import Component from './VTabBar.vue';

import RawComponent from './VTabBar.vue?raw';
import type { IStoryOptions } from '@idaproject/ui-kit/components/story/types.ts';

export const componentRaw = RawComponent;

export const category = 'Filter';

export const values: Record<string, IStoryOptions> = {
    theme: {
        default: 'light',
        vars: ['light', 'clear'],
        type: 'tabs',
    },
    size: {
        default: 'medium',
        vars: ['medium'],
    },
    specs: {
        default: [
            { label: 'Санкт-Петербург', value: 'spb' },
            { label: 'Москва', value: 'moscow' },
            { label: 'Екатеринбург', value: 'ekt' },
        ],
        type: 'readonly',
    },
    disabled: { default: false, type: 'boolean' },
    required: { default: false, type: 'boolean' },
    multiple: { default: false, type: 'boolean' },
    error: { default: false, type: 'boolean' },
    absoluteHint: { default: true, type: 'boolean' },
    msg: { default: 'msg' },
    infoRight: { default: 'infoRight' },
    prefixIcon: { default: 'file' },
    label: { default: 'Label' },
    placeholder: { default: 'placeholder' },
};

export default defineComponent({
    name: 'VTabBarDemo',
    components: { Component },

    setup(_) {
        return () => h(Component, null, {
            default: () => [],
        });
    },
});
