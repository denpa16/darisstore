import LazyLoad from 'vanilla-lazyload';

const handleSecondLoad = (el, options, log = false, binding = null) => {
    if (!el) {
        console.warn('LazyLoad: el.instance is not defined');
        return;
    }

    const lazyOptions = {
        ...options,
        data_srcset: 'lazy-srcset',
        data_sizes: 'lazy-sizes',
        data_src: 'lazy-src',
        cancel_on_exit: false,
    };

    if (el?.instance?._settings) {
        el.instance.destroy();
        ['data-ll-status', 'data-src'].forEach(attribute => el.removeAttribute(attribute));

        setTimeout(() => {
            LazyLoad.load(el, lazyOptions);
        }, 10);
    }

    if (log && binding) {
        binding.value(el);
    }
};

export default {
    bind(el, binding) {
        el.item = [];
        el.item.push(el);

        const lazyOptions = {
            use_native: false,
            threshold: 50,
            ...el.dataset,
            // cancel_on_exit: false,
        };


        /**
         * Если указаны data-lazy-srcset или data-lazy-src, то создаётся новый инстанс, чтобы после
         * подмены пустой пикчи на preview с блуром, уже блур подменялся на полноценное изображение
         */
        if (el.dataset?.lazySrcset || el.dataset?.lazySrc) {
            lazyOptions.callback_loaded = el => handleSecondLoad(el, lazyOptions, typeof binding.value === 'function', binding);
        } else if (typeof binding.value === 'function') {
            lazyOptions.callback_loaded = el => binding.value(el);
        }

        el.instance = new LazyLoad({
            ...lazyOptions,
        }, el.item);
    },

    unbind(el) {
        if (el?.instance?._settings) {
            el.instance.destroy();
        }
    },
};
