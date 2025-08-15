function inserted(el, binding) {
    const modifiers = binding.modifiers || {};
    const value = binding.value;
    const { handler, options } = typeof value === 'object'
        ? value
        : { handler: value, options: {} };

    const observer = new IntersectionObserver((entries, observer) => {
        if (!el._observe) {
            return;
        }

        const isIntersecting = Boolean(entries.find(entry => entry.isIntersecting));

        if (handler && (!modifiers.quiet || el._observe.init)) {
            handler(entries, observer, isIntersecting);
        }

        if (el._observe.init && modifiers.once || modifiers.enterOnce && isIntersecting) {
            unbind(el);
        } else {
            el._observe.init = true;
        }
    }, options);

    el._observe = { init: false, observer };

    observer.observe(el);
}

function unbind(el) {
    if (!el._observe) {
        return;
    }

    el._observe.observer.unobserve(el);
    delete el._observe;
}

export const Intersect = {
    inserted,
    unbind,
};

export default Intersect;
