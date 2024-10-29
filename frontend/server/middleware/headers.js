// eslint-disable-next-line no-undef
export default defineEventHandler(event => {
    if (!event.node.req) {
        return;
    }

    const headers = event.node.req && event.node.req.headers ? Object.assign({}, event.node.req.headers) : {};
    event.node.req.serverReferer = headers.referer;
});
