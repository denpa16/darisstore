/**
 * Решает проблемы с CORS
 */

import { createProxyEventHandler } from 'h3-proxy';
import type { EventHandler } from 'h3';

const config = useRuntimeConfig();
const API_SLUGS = ['/api', '/api2'];

function createHandler(targetUrl: string, pathPrefix: string, rewrite: string = 'api'): EventHandler | null {
    return createProxyEventHandler({
        target: targetUrl,
        changeOrigin: true,
        pathRewrite: {
            [`^${pathPrefix}`]: rewrite,
        },
        pathFilter: `${pathPrefix}/**`,
    });
}

const firstProxyHandler = config.public.PROXY_URL ? createHandler(config.public.PROXY_URL, API_SLUGS[0]) : null;
// const secondProxyHandler = createHandler(config.public.PROXY_URL2, API_SLUGS[1]);

function getProxyHandler(url: string | undefined): EventHandler | null {
    if (!url) {
        return null;
    }
    // if (url.startsWith(API_SLUGS[1]) && secondProxyHandler) {
    //     return secondProxyHandler;
    // }
    if (url.startsWith(API_SLUGS[0]) && firstProxyHandler) {
        return firstProxyHandler;
    }
    return null;
}

export default defineEventHandler(async event => {
    const proxyHandler = getProxyHandler(event.node.req.url);
    if (proxyHandler) {
        return proxyHandler(event);
    }
});
