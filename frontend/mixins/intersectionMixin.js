export const intersectionMixin = {
    data() {
        return {
            intersectionObserver: null,
            isVisible: false,
            isShown: false,
            minimalIntersectionRatio: 0,
        };
    },

    mounted() {
        this.setupIntersectionObserver();
    },

    beforeDestroy() {
        if (!this.intersectionObserver) {
            return;
        }

        this.intersectionObserver?.disconnect();
        this.intersectionObserver = null;
    },

    methods: {
        setupIntersectionObserver() {
            if (!(this.$el instanceof Element)) {
                return;
            }

            const options = { threshold: 0.8 };
            const handler = entries => {
                const [target] = entries;

                if (!target) {
                    return;
                }

                this.isVisible = entries[0]?.isIntersecting;
                this.isShown = this.isVisible || this.isShown;
            };

            this.intersectionObserver = new IntersectionObserver(handler, options);
            this.intersectionObserver.observe(this.$el);
        },
    },
};
