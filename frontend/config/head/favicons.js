// TODO: Set favicons

const faviconsLinks = [
    {
        rel: 'icon',
        href: '/favicons/favicon.ico',
    },
    {
        rel: 'apple-touch-icon',
        sizes: '180x180',
        href: '/favicons/apple-touch-icon.png',
    },
    {
        rel: 'icon',
        type: 'image/png',
        sizes: '96x96',
        href: '/favicons/favicon-96x96.png',
    },
    {
        rel: 'manifest',
        href: '/favicons/site.webmanifest',
        crossorigin: 'use-credentials',
    },
];

const faviconsMeta = [
    {
        name: 'msapplication-TileColor',
        content: '#282828',
    },
    {
        name: 'theme-color',
        content: '#ffffff',
    },
];

export { faviconsLinks, faviconsMeta };
