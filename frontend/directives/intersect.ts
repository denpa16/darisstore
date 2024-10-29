// Директива для отслеживания появления элемента на экране
// Как пользоваться: <div v-intersect="{handler: handlerFunction, options: {threshold: [0]} , rootMargin: '40px'}"></div>
// v-intersect.once - срабатывает один раз

import type { DirectiveBinding } from 'vue';

interface ExtendedHTMLElement extends HTMLElement {
    _observe?: {init: boolean, observer: IntersectionObserver}
}

type DirectiveModifiers = {once?: boolean, quiet?: boolean};

function mounted(el: ExtendedHTMLElement, binding: DirectiveBinding): void {
    const modifiers: DirectiveModifiers = binding.modifiers || {};
    const value = binding.value;
    const { handler, options } = typeof value === 'object'
        ? value
        : { handler: value, options: {} };

    const observer: IntersectionObserver = new IntersectionObserver((entries, observer) => {
        if (!el._observe) {
            return;
        }

        const isIntersecting: boolean = Boolean(entries.find(entry => entry.isIntersecting));

        if (handler && (!modifiers.quiet || el._observe.init)) {
            handler(entries, observer, isIntersecting);
        }

        if (el._observe.init && modifiers.once && isIntersecting) {
            beforeUnmount(el);
        } else {
            el._observe.init = true;
        }
    }, options);

    el._observe = { init: false, observer };

    observer.observe(el);
}

function beforeUnmount(el: ExtendedHTMLElement): void {
    if (!el._observe) {
        return;
    }

    el._observe.observer.unobserve(el);
    delete el._observe;
}

export default {
    mounted,
    beforeUnmount,
};
