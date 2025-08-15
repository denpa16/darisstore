export const proxy = () => ({
    '/api': {
        target: process.env.PROXY_URL,
    },
});
