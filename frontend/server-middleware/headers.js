export default function(req, res, next) {
    if (!req) {
        return next();
    }

    const headers = req && req.headers ? Object.assign({}, req.headers) : {};
    req.serverReferer = headers.referer;
    next();
}
