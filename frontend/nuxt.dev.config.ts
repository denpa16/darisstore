import commonModules from './config/modules/commonModules';
import devModules from './config/modules/devModules';
import fs from 'fs';
import path from 'path';

const nuxtDevConfig = {
    // Local server settings
    devServer: {
        port: 3000,
        host: '0.0.0.0',
        https: process.env.HTTPS_KEY && process.env.HTTPS_CERT
            ? {
                key: fs.readFileSync(path.resolve(__dirname, process.env.HTTPS_KEY))
                    .toString(),
                cert: fs.readFileSync(path.resolve(__dirname, process.env.HTTPS_CERT))
                    .toString(),
            }
            : false,
    },

    devtools: { enabled: true },

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
        checker: true,
    },
};

export default nuxtDevConfig;
