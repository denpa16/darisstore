let resizeObserver = null;

export default {
    mounted(el, binding) {
        if (typeof binding.value === 'function') {
            resizeObserver = new ResizeObserver(binding.value);

            resizeObserver.observe(el);
        } else {
            console.error('resize directive: argument must be a function');
        }
    },

    beforeUnmount(el) {
        resizeObserver?.unobserve(el);
    },
};
