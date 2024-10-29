import type { favIcons, headMetas } from './types';

const faviconsLinks: favIcons = [
    {
        rel: 'icon',
        href: '/favicons/favicon.ico',
    },
    {
        rel: 'apple-touch-icon',
        href: '/favicons/apple-touch-icon.png',
        sizes: '180x180',
    },
    {
        rel: 'icon',
        href: '/favicons/favicon-32x32.png',
        sizes: '32x32',
        type: 'image/png',
    },
    {
        rel: 'icon',
        href: '/favicons/favicon-16x16.png',
        sizes: '16x16',
        type: 'image/png',
    },
    {
        rel: 'manifest',
        href: '/favicons/site.webmanifest',
        crossorigin: 'use-credentials',
    },
    {
        rel: 'mask-icon',
        href: '/favicons/safari-pinned-tab.svg',
        color: '#1a1b1d',
    },
];

const faviconsMeta: headMetas = [
    {
        name: 'msapplication-TileColor',
        content: '#1a1b1d',
    },
    {
        name: 'theme-color',
        content: '#1a1b1d',
    },
];

export { faviconsLinks, faviconsMeta };
