import type { IncomingHttpHeaders } from 'http';
import type { RuntimeConfig } from 'nuxt/schema';
import type { QueryObject } from 'ufo';
import type { H3Event } from 'h3';

export interface IMultiCacheOptions {
    event: H3Event;
    buildReturn: string;
    requestEnabled: boolean;
}

export interface IHandleQuery {
    query: QueryObject;
    path: string;
}

export interface IGetCacheKey {
    base: string;
    domain: string;
    userAgent: string,
    acceptFormats: string,
    deviceType: 'mobile' | 'desk',
    isSafari: boolean,
    imgFormat: 'webp' | 'png',
    matches: RegExpMatchArray | null,
    versionNum: number,
    queryString: string,
    runtimeConfig: RuntimeConfig,
    queryAllowedArr: string[],
}

export interface IGetIsCacheAllowed {
    base: string;
    runtimeConfig: RuntimeConfig,
    pattern: RegExp,
    blacklistArr: string[],
    whitelistArr: string[],
    yandexRefs: string[],
    headers: IncomingHttpHeaders,
    referer: string
}
