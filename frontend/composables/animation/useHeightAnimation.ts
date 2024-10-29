import { gsap } from 'gsap';

interface heightAnimationOptions {
    element?: HTMLElement
    duration?: number,
    heightFrom?: number | string
    heightTo?: number
    isActive?: boolean
}

export function useHeightAnimation(options: heightAnimationOptions) {
    // #region Data
    const duration = ref<number>(options.duration || 0.4);
    const heightTo = ref<number | string>(options.heightTo || 'auto');
    const heightFrom = ref<number | string>(options.heightFrom || 0);
    // #endregion

    // #region Methods
    function animate() {
        if (!options.element) {
            return;
        }

        if (options.isActive) {
            gsap.to(options.element, {
                duration: duration.value,
                height: heightTo.value,
            });
        } else {
            gsap.to(options.element, {
                duration: duration.value,
                height: heightFrom.value,
            });
        }
    }

    // #endregion

    return {
        animate,
    };
}
