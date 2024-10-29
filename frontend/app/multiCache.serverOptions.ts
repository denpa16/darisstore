import { defineMultiCacheOptions } from 'nuxt-multi-cache/dist/runtime/serverOptions';
import { getHeader, getQuery } from 'h3';
import { hasTrailingSlash, parseQuery, stringifyQuery } from 'ufo';

import type { IGetCacheKey, IGetIsCacheAllowed, IHandleQuery, IMultiCacheOptions } from './types';


/**
 * Checks query params with or without trailing slash
 * and generates needed prefix key for caching
 * @param {H3Event} event
 * @returns {string} prefix key
 */
function handleQuery(event: IMultiCacheOptions['event']): string {
    const path: IHandleQuery['path'] = event.path;
    let query: IHandleQuery['query'] = getQuery(event) || {};


    if (!Object.keys(query).length && hasTrailingSlash(path, true) && path.split('?').length > 1) {
        query = parseQuery(path.replace(/\/(\?|$)/, '$1'));
    }

    if (!Object.keys(query).length) {
        return '';
    }

    return `:query_${stringifyQuery(query)}`;
}

/**
 * Generates cache key prefix base on headers of client,
 * what allowed to separate cache by device type.
 * Also separate cache with and without query params if they allowed in runtimeConfig.CACHE_ALLOW_QUERY
 * @param {H3Event} event
 * @returns {string} cache key
 */
function getCacheKey(event: IMultiCacheOptions['event']): string {
    let routePath: IGetCacheKey['base'] = event.path.split('?')[0];

    // Удаление cлэш на конце
    if (routePath.length > 1 && routePath.endsWith('/')) {
        routePath = routePath.slice(0, -1);
    }

    // Headers
    const domain: IGetCacheKey['domain'] = getHeader(event, 'x-forwarded-host') || 'domain';
    const userAgent: IGetCacheKey['userAgent'] = getHeader(event, 'user-agent') || '';
    const acceptFormats: IGetCacheKey['acceptFormats'] = getHeader(event, 'accept') || '';

    // Types of device
    const deviceType: IGetCacheKey['deviceType'] = /Mobi/i.test(userAgent) ? 'mobile' : 'desk';
    const isSafari: IGetCacheKey['isSafari'] = /^((?!chrome|android).)*safari/i.test(userAgent);
    let imgFormat: IGetCacheKey['imgFormat'] = /\b(webp)\b/i.test(acceptFormats) ? 'webp' : 'png';

    if (isSafari) {
        const matches: IGetCacheKey['matches'] = userAgent.match(/Version\/(\d+(?:\.\d+)?)/);

        if (matches?.length) {
            const versionNum: IGetCacheKey['versionNum'] = parseFloat(matches[1]);
            if (versionNum >= 16) {
                imgFormat = 'webp';
            }
        }
    }

    // Allow query cache
    let queryString: IGetCacheKey['queryString'] = '';

    const runtimeConfig: IGetCacheKey['runtimeConfig'] = useRuntimeConfig();
    const queryAllowedArr: IGetCacheKey['queryAllowedArr'] = typeof runtimeConfig?.CACHE_ALLOW_QUERY === 'string'
        ? runtimeConfig.CACHE_ALLOW_QUERY
            .split(' ')
        : [];


    if (queryAllowedArr?.includes(routePath)) {
        queryString = handleQuery(event);
    }

    return `${domain}:${deviceType}:${imgFormat}${queryString}--${routePath || 'homepage'}/`;
}

/**
 * Check if we allow pages to cache by blacklist or whitelist,
 * It will depend on runtimeConfig – CACHE_PAGES_BLACKLIST || CACHE_PAGES_WHITELIST.
 * This function will block caching pages if they respond in Yandex Metrik iframe.
 * @param event
 * @returns {boolean} is allowed
 */
function getIsCacheAllowed(event: IMultiCacheOptions['event']): boolean {
    const base: IGetIsCacheAllowed['base'] = event.path.split('?')[0];
    const runtimeConfig: IGetIsCacheAllowed['runtimeConfig'] = useRuntimeConfig();

    const regexUtm = /utm_source|utm_medium|utm_term|utm_campaign|utm_content/;
    if (regexUtm.test(event.path)) {
        if (runtimeConfig.public.IS_DEV) {
            console.warn(`Route ${event.path} - found utm tags, cache is disabled`);
        }
        return false;
    }

    const blacklistArr: IGetIsCacheAllowed['blacklistArr'] = typeof runtimeConfig?.CACHE_PAGES_BLACKLIST === 'string'
        ? runtimeConfig.CACHE_PAGES_BLACKLIST
            .split(' ')
        : [];

    const whitelistArr: IGetIsCacheAllowed['whitelistArr'] = typeof runtimeConfig?.CACHE_PAGES_WHITELIST === 'string'
        ? runtimeConfig.CACHE_PAGES_WHITELIST
            .split(' ')
        : [];

    // Black list or white list check
    if (blacklistArr.length) {
        const pattern: IGetIsCacheAllowed['pattern'] = new RegExp(`^(${blacklistArr.join('|')})(\\/|$)|(^|\\/+)(${blacklistArr.join('|')})(\\/|$)`);

        if (pattern.test(base)) {
            if (runtimeConfig.public.IS_DEV) {
                console.warn(`Route ${base} is found in blacklist array and will not be caching`);
            }
            return false;
        }
    } else if (whitelistArr.length) {
        const pattern: IGetIsCacheAllowed['pattern'] = new RegExp(`^(${whitelistArr.join('|')})(\\/|$)|(^|\\/+)(${whitelistArr.join('|')})(\\/|$)`);

        if (!pattern.test(base)) {
            if (runtimeConfig.public.IS_DEV) {
                console.warn(`Route ${base} is not found in whitelist array and will not be caching`);
            }
            return false;
        }
    }

    // Cache disabled if Yandex Metrik ref
    const yandexRefs: IGetIsCacheAllowed['yandexRefs'] = [
        'https://metrika.yandex.by/',
        'http://metrika.yandex.by/',
        'https://metrica.yandex.com.tr/',
        'http://metrica.yandex.com.tr/',
        'https://metrika.yandex.ru/',
        'http://metrika.yandex.ru/',
        'https://metrica.yandex.com/',
        'http://metrica.yandex.com/',
        'https://webvisor.com/',
        'http://webvisor.com/',
    ];

    const headers: IGetIsCacheAllowed['headers'] = event.node.req && event.node.req.headers ? Object.assign({}, event.node.req.headers) : {};
    const referer: IGetIsCacheAllowed['referer'] = headers.referer || '';

    if (referer && yandexRefs.includes(referer)) {
        if (runtimeConfig.public.IS_DEV) {
            console.warn(`Referer ${referer} is found in yandexRefs array and will not be caching`);
        }
        return false;
    }

    // Caches enabled for anonymous users.
    return true;
}

/**
 * Reed more about module configuration in https://nuxt-multi-cache.dulnan.net/features/route-cache
 */
export default defineMultiCacheOptions({
    route: {
        buildCacheKey: (event: IMultiCacheOptions['event']): IMultiCacheOptions['buildReturn'] => getCacheKey(event),
    },

    enabledForRequest: (event: IMultiCacheOptions['event']): Promise<IMultiCacheOptions['requestEnabled']> => Promise.resolve(getIsCacheAllowed(event)),
});
