interface Breadcrumb {
    title: string;
    link: string;
    disabled?: boolean;
}

export interface Props {
    size?: 'small' | 'medium',
    color?: 'base' | 'dark',
    breadcrumbs: Array<Breadcrumb>,
    separator?: 'slash' | 'point',
    name?: '',
}
