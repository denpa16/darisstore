import path from 'path';
import { defineNuxtConfig } from 'nuxt/config';
import upath from 'upath';
import nuxtDevConfig from './nuxt.dev.config';
import nuxtProdConfig from './nuxt.prod.config';
import headConfig from './config/headConfig.js';
import extendRoutesConfig from './config/extendRoutesConfig';

const pathAssets = upath.toUnix(path.resolve(__dirname, './assets'));
const isDev = process.env.NODE_ENV === 'development';
const isProd = !process.env.PROXY_URL && process.env.SERVER_API_URL === 'https://template.idacloud.ru/';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    extends: [
        '@idaproject/core',
        '@idaproject/device',
        '@idaproject/image',
        '@idaproject/filter',
        '@idaproject/ymaps3',
        '@idaproject/genplan',
        '@idaproject/ui-kit',
    ],

    ...isDev ? nuxtDevConfig : nuxtProdConfig,

    runtimeConfig: {
        PROXY_URL: process.env.PROXY_URL,
        // PROXY_URL2: process.env.PROXY_URL2,
        SERVER_API_URL: process.env.SERVER_API_URL,
        DEVELOPMENT: isDev,
        CACHE_PAGES_BLACKLIST: '/favorites /lk /ui-kit',
        CACHE_ALLOW_QUERY: '/projects',
        SENTRY_DSN_FRONTEND: process.env.SENTRY_DSN_FRONTEND,
        SENTRY_ENVIRONMENT: process.env.SENTRY_ENVIRONMENT,
        // CACHE_PAGES_WHITELIST: '/projects',

        public: {
            sentry: {
                dsn: process.env.SENTRY_DSN_FRONTEND,
                environment: process.env.SENTRY_ENVIRONMENT,
            },
            DOMAIN: process.env.PROXY_URL || process.env.SERVER_API_URL,
            IS_DEV: isDev,
            IMGPROXY_SITE_HOST: process.env.IMGPROXY_SITE_HOST,
            CAPTCHA: process.env.CAPTCHA,
            CAPTCHA_TEST: process.env.CAPTCHA_TEST,
            PROXY_URL: process.env.PROXY_URL,
            // PROXY_URL2: process.env.PROXY_URL2,
            SERVER_API_URL: process.env.SERVER_API_URL,
        },
    },

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // MAIN SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    app: {
        // Head section
        // @ts-expect-error TODO: разобраться что там ему именно надо
        head: headConfig,
    },

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // ROUTES / HOOKS SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    router: {
        options: {
            linkActiveClass: '_active-link',
            linkExactActiveClass: '_exact-link',
        },
    },

    routeRules: {
        '/dev/**': isProd ? { redirect: '/' } : undefined,
        '/': { delayHydration: false },
        '/ui-kit/*': { delayHydration: false },
    },

    hooks: {
        // prevent some prefetch behaviour
        'build:manifest': manifest => {
            for (const key in manifest) {
                manifest[key].dynamicImports = [];

                const file = manifest[key];
                if (file.assets) {
                    file.assets = file.assets.filter(assetName => !/.+\.(gif|jpe?g|png|svg|webp)$/.test(assetName));
                }
            }
        },

        // Замена extendroutes из nuxt2
        'pages:extend'(pages) {
            extendRoutesConfig(pages, path.resolve(__dirname, ''));
        },
    },

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // COMPONENTS CONFIGURATION SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    svgSprite: {
        // Disabled _icons page from svgSprite http://127.0.0.1:3000/_icons
        // iconsPath: null,
    },

    // PartyTown module – https://nuxt.com/modules/partytown
    partytown: {
        debug: isDev,
        lib: '~partytown',
        forward: ['ym'],
    },

    // Cache, configuration file is frontend/app/multiCache.serverOptions.ts
    multiCache: {
        api: {
            enabled: !isDev,
        },
        route: {
            enabled: !isDev,
        },
        debug: isDev,
    },

    // Nuxt-delay-hydration
    delayHydration: {
        mode: 'mount',
        postIdleTimeout: { mobile: 3000, desktop: 4000 },
        debug: isDev,
    },

    yandexMaps: {
        apikey: process.env.YMAPS_KEY || '9479b819-053e-481c-a7c1-82089cb0954a',
    },

    // Auto import UI components
    components: [{
        path: '~/components/ui',
        extensions: ['.vue'],
        pathPrefix: false,
    }],

    // Global CSS
    css: [
        '~/assets/scss/bundle.scss',
        '~/assets/scss/vendors.scss',
        '~/assets/scss/default.scss',
    ],

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // VITE / BUILDER CONFIGURATION SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    vite: {
        server: {
            hmr: {
                clientPort: 3000,
            },
        },

        vue: {
            script: {
                propsDestructure: true,
            },
        },

        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: `@import "${pathAssets}/scss/shared/variables"; @import "${pathAssets}/scss/shared/mixins"; @import "${pathAssets}/scss/shared/functions";`,
                },
            },
        },

        optimizeDeps: {
            exclude: ['fsevents'],
            entries: ['@idaproject/**/*.{vue,js,jsx,ts,tsx}'],
        },

        build: {
            cssCodeSplit: true,
            cssMinify: 'esbuild',
            rollupOptions: {
                output: {
                    experimentalMinChunkSize: 340 * 1024,
                    manualChunks: (id, _) => {
                        if (
                            !id.includes('node_modules') &&
                          !id.startsWith('virtual:') &&
                          !id.includes('src') &&
                          !id.includes('index') &&
                          !id.includes('assets')
                        ) {
                            if (id.includes('pages')) {
                                const parts = id.split('/');
                                const folderIndex = parts.indexOf('pages');
                                if (folderIndex + 2 < parts.length) {
                                    const pageGroup = parts[folderIndex + 1];
                                    return `chunk-pg-${pageGroup}`;
                                }
                                return 'chunk-pg-misc';
                            }
                        }
                    },
                },
            },
        },
    },
});
