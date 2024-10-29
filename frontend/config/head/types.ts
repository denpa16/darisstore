export interface faviconItem {
    rel?: string,
    href?: string,
    sizes?: string,
    type?: string,
    crossorigin?: string,
    color?: string,
}

export interface metaItem {
    name?: string,
    content?: string,
}

export type favIcons = faviconItem[];
export type headMetas = metaItem[];
