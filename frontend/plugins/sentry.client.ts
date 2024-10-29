import * as Sentry from '@sentry/vue';
import { SENTRY_IGNORE_LIST_URL } from '@/assets/ts/constants/sentry.ts';

export default defineNuxtPlugin(nuxtApp => {
    const router = useRouter();
    const runtimeConfig = useRuntimeConfig();
    const allowUrl = runtimeConfig.public.SERVER_API_URL as string;
    const { public: { sentry, IS_DEV } } = useRuntimeConfig();

    if (!sentry.dsn || IS_DEV || !allowUrl) {
        return;
    }

    Sentry.init({
        app: nuxtApp.vueApp,
        dsn: sentry.dsn,
        environment: sentry.environment,

        // Не трекаем запросы которые не включают наш боевой домен
        beforeSend(event) {
            if (!event?.request?.url?.includes(window.location.host)) {
                return null;
            }

            return event;
        },

        integrations: [
            new Sentry.BrowserTracing({
                routingInstrumentation: Sentry.vueRouterInstrumentation(router),
            }),
            new Sentry.Replay(),
        ],

        // Отключение отправки транзакций на сторонние скрипты
        ignoreErrors: SENTRY_IGNORE_LIST_URL,
        ignoreTransactions: SENTRY_IGNORE_LIST_URL,
        denyUrls: SENTRY_IGNORE_LIST_URL,

        allowUrls: [allowUrl],

        // Configure this whole part as you need it!

        tracesSampleRate: 0.01, // Change in prod

        // Set `tracePropagationTargets` to control for which URLs distributed tracing should be enabled
        tracePropagationTargets: [allowUrl],

        replaysSessionSampleRate: 1.0, // Change in prod
        replaysOnErrorSampleRate: 1.0, // Change in prod if necessary
    });
});
