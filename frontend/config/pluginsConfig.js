const pluginsConfig = [
    '~/config/plugins/axios',
    '~/config/plugins/modal',
    '~/config/plugins/api',
    '~/config/plugins/vue-touch-events',
    {
        src: '~/config/plugins/gsap.js', mode: 'client',
    },
    {
        src: '~/config/plugins/swiper', mode: 'client',
    },
    {
        src: '~/directives/index', mode: 'client',
    },
];

export default pluginsConfig;
