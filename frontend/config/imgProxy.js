import { joinURL } from 'ufo';
import { createOperationsGenerator } from '~/assets/js/utils/image-utils';
// import { getFileExtension } from '~/assets/js/utils/file-utils';

const operationsGenerator = createOperationsGenerator({
    keyMap: {
        width: 'w',
        height: 'h',
        fit: 'rt',
        position: 'g',
        quality: 'q',
        blur: 'bl',
        background: 'bg',
    },

    valueMap: {
        fit: {
            cover: 'fill',
            contain: 'fit',
            fill: 'force',
        },
        position: {
            smart: 'sm',
            center: 'ce',
            top: 'no',
            bottom: 'so',
            right: 'ea',
            left: 'we',
            'top-right': 'noea',
            'top-left': 'nowe',
            'bottom-right': 'soea',
            'bottom-left': 'sowe',
        },
    },

    joinWith: '/',
    formatter: (key, value) => `${key}:${value}`,
});

export function getImage(
    src,
    { modifiers, baseURL, quality, staticFolder },
    { nuxtContext, options },
) {
    let format = null;
    let source = src;
    const ex = src.match(/\.[^.]+$/g);
    const fileExtension = ex[0]?.substring(1) || '';

    // если развернуто локально и используются изображения из статики
    // то возвращаем оригинальный url или если нет ссылки на proxy или если закидывается свг
    // внимание!!! На тесте будет работать только когда снимется пароль
    if (nuxtContext.isDev && /^\/images\//g.test(source) || !baseURL || fileExtension === 'svg') {
        return {
            url: source,
        };
    }

    // Check if image is static
    const reg = new RegExp(`^${staticFolder}.*$`, 's');
    if (src.match(reg)) {
        const domain = nuxtContext.store.getters['domain/getDomainAddress'];
        source = `${domain}${src}`;
    }

    // Is Webp supported
    const isWebSup = nuxtContext.store.getters['device/getIsWebpSupported'] ? 'webp' : 'png';

    // Check image format
    if (modifiers?.format) {
        format = modifiers.format === 'webp' && !isWebSup ? 'png' : modifiers.format;
        delete modifiers.format;
    } else {
        format = isWebSup ? 'webp' : 'png';
    }

    // Modifiers
    let defaultModifiers = {};

    if (modifiers?.preset) {
        defaultModifiers = options.presets[modifiers?.preset]?.modifiers || {};
        if (!Object.keys(defaultModifiers)?.length) {
            console.warn(`preset: ${modifiers.preset} not found`);
        }

        delete modifiers.preset;
    } else if (!modifiers?.quality) {
        defaultModifiers.quality = quality;
    }

    // Changes resolution of source for preview images by 2
    if (modifiers.blur) {
        modifiers.dpr = 0.5;
    }

    const operationsString = operationsGenerator({ ...modifiers, ...defaultModifiers });

    return {
        url: joinURL(`${baseURL}/insecure`, operationsString, `plain/${source}@${format}`),
    };
}
