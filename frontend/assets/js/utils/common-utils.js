import {gsap} from 'gsap/dist/gsap.js';
import {ScrollToPlugin} from 'gsap/dist/ScrollToPlugin.js';

gsap.registerPlugin(ScrollToPlugin);

export function scrollTo(id = false, offset = 0, force = false) {
    const target = document.getElementById(id || '__nuxt');
    const header = document.getElementById('header');
    const headerHeight = header?.offsetHeight || 0;

    if (target) {
        const position = target.getBoundingClientRect().top + window.pageYOffset;

        if (force) {
            window.scroll({
                top: position - offset,
                left: 0,
                behavior: 'instant',
            });
        } else {
            gsap.to(window, {
                duration: .5,
                scrollTo:
                    { y: position, offsetY: offset || headerHeight },
            });
        }
    }
}
