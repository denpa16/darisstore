import {
    faviconsLinks,
    faviconsMeta,
} from './head/favicons';

import {
    headScripts,
    headNoScripts,
} from './head/scripts';

const headConfig = {
    htmlAttrs: { lang: 'ru' },

    title: 'IDA Template',

    // Head meta
    meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'theme-color', content: '#111' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },

        // Favicons
        ...faviconsMeta,
    ],

    // Head links
    link: [
        // Favicons
        ...faviconsLinks || {},
    ],

    script: process.env.GTM !== 'False'
        ? [...headScripts]
        : [],

    noscript: process.env.GTM !== 'False'
        ? [...headNoScripts]
        : [],

    __dangerouslyDisableSanitizers: ['script', 'noscript'],
};

export default headConfig;
