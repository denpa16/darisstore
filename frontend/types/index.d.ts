declare global {
    interface Window {
        dataLayer: Record<string, any>[];
        gtag: Record<string, any>[];
        ga: Record<string, any>[];
    }
}
