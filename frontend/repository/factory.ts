import type { $Fetch } from 'ofetch';

// Регулярка с адресом моковых АПИ
const MOCK_API_PATH: RegExp = /^\/mock-api\//;

class HttpFactory {
    private readonly $fetch: $Fetch;

    constructor(fetcher: $Fetch) {
        this.$fetch = fetcher;
    }

    /**
     * method - GET, POST, PUT
     * URL
     */
    async call<T>(method: string, url: string, data: object|FormData = {}, extras = {}): Promise<T> {
        const options: {baseURL?: string} = {};

        if (MOCK_API_PATH.test(url)) {
            options.baseURL = this.getBaseURL();
        }

        const requestData = data instanceof FormData ? { body: data } : data;
        try {
            const $res: T = await this.$fetch(url, { method, ...requestData, ...options, ...extras });
            return $res;
        } catch (error) {
            throw new Error(error as string);
        }
    }

    /**
     * Отдает базовый URL для запросов.
     * Если обращение идет к моковым АПИ, и это локальный сервер
     * То, меняем baseURL, чтобы запросы шли на локальный Dev Server Nuxt'а, а не улетали на тестовый
     * Чтобы работал HTTPS с моковыми АПИ, нужно добавить в env NODE_TLS_REJECT_UNAUTHORIZED=0
     * @private
     */
    private getBaseURL(): string | undefined {
        let baseURL = process.env?.SERVER_API_URL;

        if (process.env?.PROXY_URL) {
            baseURL = JSON.parse(process.env?.__NUXT_DEV__ || '')?.proxy?.url || 'http://localhost:3000/';
        }

        if (import.meta.client) {
            baseURL = `${location.origin}/`;
        }

        return baseURL;
    }
}

export default HttpFactory;
