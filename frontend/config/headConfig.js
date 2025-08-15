import {
    faviconsLinks,
    faviconsMeta,
} from './head/favicons';

import {
    headScripts,
    headNoScripts,
} from './head/scripts';
import { SITE_DESCRIPTION, SITE_IMAGE, SITE_PAGE, SITE_URL } from '../assets/js/constants/index.js';

const headConfig = {
    htmlAttrs: { lang: 'ru' },

    title: SITE_PAGE,

    // Head meta
    meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0' },

        { hid: 'description', name: 'description', content: SITE_DESCRIPTION },

        // Open Graph / Facebook / WhatsApp
        { hid: 'og:type', name: 'og:type', content: 'website' },
        { hid: 'og:url', name: 'og:url', content: SITE_URL },
        { hid: 'og:title', name: 'og:title', content: SITE_PAGE },
        {
            hid: 'og:site_name',
            name: 'og:site_name',
            content: SITE_PAGE,
        },
        {
            hid: 'og:description',
            name: 'og:description',
            content: SITE_DESCRIPTION,
        },
        { hid: 'og:image', name: 'og:image', content: SITE_IMAGE },
        { hid: 'og:image:width', name: 'og:image:width', content: '300' },
        { hid: 'og:image:height', name: 'og:image:height', content: '300' },

        // Twitter
        {
            hid: 'twitter:card',
            name: 'twitter:card',
            content: 'summary_large_image',
        },
        { hid: 'twitter:url', name: 'twitter:url', content: SITE_URL },
        {
            hid: 'twitter:title',
            name: 'twitter:title',
            content: SITE_PAGE,
        },
        {
            hid: 'twitter:description',
            name: 'twitter:description',
            content: SITE_DESCRIPTION,
        },
        { hid: 'twitter:image', name: 'twitter:image', content: SITE_IMAGE },

        { name: 'theme-color', content: '#111' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },

        // Favicons
        ...faviconsMeta,
    ],

    // Head links
    link: [
        // Favicons
        ...faviconsLinks,
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
