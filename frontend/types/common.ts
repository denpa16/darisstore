export interface headScriptItem {
    innerHTML?: string,
    async?: boolean,
    defer?: boolean,
    body?: boolean
    src?: string
}

export type headScriptList = headScriptItem[];

export type errorStatusCodes = 404 | 500 | 502 | 505;
