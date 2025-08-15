const commonModules = [
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
    '@nuxtjs/style-resources',
    'nuxt-device-is',
    '@nuxt/components',
    'nuxt-ssr-cache',
    'nuxt-delay-hydration',
    // Надстройка над модулем nuxt-delay-hydration для добавления списка исключений страниц,
    // Список исключения виде массива, начинаться должны с '/' (учитывает все subpages.
    // ['~/config/modules/nuxtDelayHydrationExclude', {excludePaths: ['/']}],
];

export default commonModules;
