import commonModules from './config/modules/commonModules';
import devModules from './config/modules/devModules';
import { proxy } from './config/proxy';

const nuxtDevConfig = {
    modules: [
        ...commonModules,
        ...devModules,
    ],

    // Stylelint options
    stylelint: {
        files: [
            'assets/**/*.{s?(a|c)ss}',
            '**/components/**/*.{s?(a|c)ss}',
            '**/{components,layouts,services,pages}/**/*.vue',
        ],
    },

    // Eslint options
    eslint: {
        cache: false,
    },

    /**
     * Модуль прокси решает проблемы с CORS, используется только на локалке
     */
    proxy: process.env.PROXY_URL ? proxy() : {},
};

export default nuxtDevConfig;
