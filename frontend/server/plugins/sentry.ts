// On the top of the file, import H3Error!
import { H3Error } from 'h3';
import * as Sentry from '@sentry/node';
import { ProfilingIntegration } from '@sentry/profiling-node';

export default defineNitroPlugin(nitroApp => {
    const { public: { sentry, IS_DEV } } = useRuntimeConfig();

    if (IS_DEV) {
        return;
    }

    // If no sentry DSN set, ignore and warn in the console
    if (!sentry.dsn) {
        console.warn('Sentry DSN not set, skipping Sentry initialization');
        return;
    }

    // Initialize Sentry
    Sentry.init({
        dsn: sentry.dsn,
        environment: sentry.environment,
        integrations: [
            new ProfilingIntegration(),
        ],
        // Performance Monitoring
        tracesSampleRate: 0.01, // Change in production!
        // Set sampling rate for profiling - this is relative to tracesSampleRate
        profilesSampleRate: 0.01, // Change in production!
    });

    // Here comes the hooks
    nitroApp.hooks.hook('error', error => {
        // Do not handle 404s and 422s
        if (error instanceof H3Error) {
            if (error.statusCode === 404 || error.statusCode === 422) {
                return;
            }
        }
        Sentry.captureException(error);
    });

    nitroApp.hooks.hook('request', event => {
        event.context.$sentry = Sentry;
    });

    nitroApp.hooks.hookOnce('close', async () => {
        await Sentry.close(2000);
    });
});
