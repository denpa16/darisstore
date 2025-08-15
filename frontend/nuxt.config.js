import fs from 'fs';
import path from 'path';
import nuxtDevConfig from './nuxt.dev.config';
import nuxtProdConfig from './nuxt.prod.config';
import headConfig from './config/headConfig';
import pluginsConfig from './config/pluginsConfig';

const env = {
    SERVER_API_URL: process.env.SERVER_API_URL,
    CLIENT_API_URL: process.env.CLIENT_API_URL,
    PROXY_URL: process.env.PROXY_URL,
    HTTPS_KEY: process.env.HTTPS_KEY,
    HTTPS_CERT: process.env.HTTPS_CERT,
    DEVELOPMENT: process.env.NODE_ENV === 'development',
    IMGPROXY_SITE_HOST: process.env.IMGPROXY_SITE_HOST,
    REDIS_DSN: process.env.REDIS_DSN,
    SENTRY_DSN_FRONTEND: process.env.SENTRY_DSN_FRONTEND,
    SENTRY_ENVIRONMENT: process.env.SENTRY_ENVIRONMENT,
};

const isDev = process.env.NODE_ENV === 'development';

// NuxtDeviceIs breakpoints
const breakpoints = {
    mobile: 767,
    tablet: 1279,
    laptop: 1439,
    desktop: 999999,
};

module.exports = {
    telemetry: false,

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // MAIN SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Server settings
    server: {
        port: 3000,
        host: '0.0.0.0',
        https: env.HTTPS_KEY && env.HTTPS_CERT
            ? {
                key: fs.readFileSync(path.resolve(__dirname, env.HTTPS_KEY)),
                cert: fs.readFileSync(path.resolve(__dirname, env.HTTPS_CERT)),
            }
            : null,
    },

    render: {
        http2: {
            push: true,
        },

        resourceHints: false,
    },

    // * Customize the progress-bar color
    loading: {
        color: '#d9ff6c', height: '2px', throttle: 0,
    },

    // Head section
    head: headConfig,

    // Plugins
    plugins: pluginsConfig,

    // Public env config
    publicRuntimeConfig: {
        IS_DEV: isDev,
        PROXY_URL: env.PROXY_URL,
        IMGPROXY_SITE_HOST: env.IMGPROXY_SITE_HOST,
        REDIS_DSN: env.REDIS_DSN,
        SENTRY_ENVIRONMENT: env.SENTRY_ENVIRONMENT,
    },

    // Router settings
    router: {
        linkActiveClass: '_active-link',
        linkExactActiveClass: '_exact-link',
    },

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // MAIN CONFIG EXTENDS
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    ...isDev ? nuxtDevConfig : nuxtProdConfig,

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // MODULES SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    buildModules: ['@nuxt/image', '@nuxtjs/svg-sprite'],

    serverMiddleware: [
        '~/server-middleware/headers',
    ],

    // Axios && proxy
    axios: {
        progress: false,
        ...!env.PROXY_URL && { baseURL: env.SERVER_API_URL || '' },
        ...!env.PROXY_URL && { browserBaseURL: env.CLIENT_API_URL || '' },
        proxy: Boolean(env.PROXY_URL),
    },

    // Disabled _icons page from svgSprite
    svgSprite: {
        iconsPath: null,
    },

    // NuxtDeviceIs breakpoints
    NuxtDeviceIs: {
        breakpoints,
    },

    // Auto import UI components
    components: [{
        path: '~/components/ui',
        extensions: ['vue'],
        pathPrefix: false,
        isAsync: true,
        prefetch: !isDev,
    }],

    // Nuxt images module
    image: {
        provider: 'imgProxy',
        domains: [env.SERVER_API_URL || env.PROXY_URL, 'storage.yandexcloud.net'],
        screens: { ...breakpoints, desktop: 1920 },

        intersectOptions: { // Intersection observer settings for native lazy
            rootMargin: '50px',
        },

        presets: {
            preview: {
                modifiers: {
                    quality: 20,
                    blur: 30,
                },
            },
        },

        providers: {
            imgProxy: {
                provider: '~/config/imgProxy',

                options: {
                    baseURL: env.IMGPROXY_SITE_HOST, // imgProxy service url
                    staticFolder: '/images', // redirect to internal url, if url from static folder
                    quality: 80, // Default quality
                },
            },
        },
    },

    // Nuxt-delay-hydration
    delayHydration: {
        mode: 'mount',
        postIdleTimeout: { mobile: 10000, desktop: 9000 },
        debug: isDev,
    },

    // Cache
    cache: !isDev && {
        useHostPrefix: false,

        pages: ['/'],

        key(route, context) {
            // Список исключений
            const blacklist = ['/lk'];
            const pattern = new RegExp(`^(${blacklist.join('|')})(\\/|$)|(^|\\/+)(${blacklist.join('|')})(\\/|$)`);
            const yandexRefs = ['https://metrika.yandex.ru/', 'https://metrica.yandex.com/', 'https://webvisor.com/', 'http://webvisor.com/'];
            const referer = context.req?.serverReferer;

            if (pattern.test(route) || yandexRefs.includes(referer)) {
                return false;
            }

            const domain = context.req?.headers['x-forwarded-host'];
            const userAgent = context.req?.headers['user-agent'];
            const device = /Mobi/i.test(userAgent) ? 'mobile' : 'desk';
            const isSafari = /^((?!chrome|android).)*safari/i.test(userAgent);
            let imgFormat = /\b(webp)\b/i.test(context.req?.headers['accept']) ? 'webp' : 'png';

            if (isSafari) {
                const matches = userAgent.match(/Version\/(\d+(?:\.\d+)?)/);

                if (matches?.length) {
                    const versionNum = parseFloat(matches[1]);
                    if (versionNum >= 16) {
                        imgFormat = 'webp';
                    }
                }
            }

            if (route === '/') {
                return `${domain}:${device}:${imgFormat}:page:home:string`;
            }

            let page = route.substr(1)
                .split('/');
            page = page.join('.');
            return `${domain}:${device}:${imgFormat}:page:${page}:string`;
        },

        // Настройки размера и типа кэша
        //
        // https://www.npmjs.com/package/nuxt-ssr-cache
        // Можно поменять размер кэша, время храненение
        // и даже тип кэширование, например на redis.
        // В целом текущие настройки - являются оптимальными.
        store: env.REDIS_DSN
            ? {
                type: 'redis',
                url: env.REDIS_DSN,
                ttl: 60,
                configure: [['maxmemory', '1024mb'], ['maxmemory-policy', 'allkeys-lru']],
            }
            : {
                type: 'memory', max: 500, ttl: 60,
            },
    },

    // Global CSS
    css: [
        '~/assets/scss/bundle.scss',
        '~/assets/scss/vendors.scss',
        '~/assets/scss/default.scss',
    ],

    styleResources: {
        scss: '~/assets/scss/shared/*.scss',
        hoistUseStatements: true,
    },

    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // BUILD SECTION
    // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    build: {
        publicPath: '/n/',

        analyze: isDev,

        // Set libraries to transpile by babel
        transpile: !isDev && [],

        babel: {
            presets({ envName }) {
                return [
                    [
                        '@nuxt/babel-preset-app',
                        {
                            corejs: { version: 3 },
                        },
                    ],
                ];
            },
        },

        loaders: {
            scss: {
                sourceMap: isDev,
            },
            vue: {
                cacheBusting: false,
            },
        },

        // Terser settings
        terser: !isDev && {
            terserOptions: {
                mangle: {
                    safari10: true,
                },
            },
        },

        // Postcss settings
        postcss: !isDev && {
            preset: {
                autoprefixer: {
                    grid: true,
                },
            },
        },

        extend(config, ctx) {
            // Fixes npm packages that depend on `fs` module
            config.node = {
                fs: 'empty',
            };
        },

        optimization: {
            splitChunks: {
                maxSize: 300000,
            },
        },
    },
};
