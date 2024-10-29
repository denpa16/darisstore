import { defineComponent, h } from 'vue';
import Component from './VTextArea.vue';

import RawComponent from './VTextArea.vue?raw';
import type { IStoryOptions } from '@idaproject/ui-kit/components/story/types.ts';

export const componentRaw = RawComponent;

export const category = 'Base';

export const values: Record<string, IStoryOptions> = {
    disabled: { default: false, type: 'boolean' },
    required: { default: false, type: 'boolean' },
    modelValue: { default: '', type: 'input' },
    placeholder: { default: 'placeholder', type: 'input' },
    label: { default: 'Label', type: 'input' },
    msg: { default: 'msg' },
};

export default defineComponent({
    name: 'VTextAreaDemo',
    components: { Component },

    setup(_) {
        return () => h(Component, null, {
            default: () => [],
        });
    },
});
