import type { FlatCard } from '~/repository/modules/flats/types';

type Metro = {
    name: string;
    color: string,
};

type Project = {
    metro: Metro;
    name: string;
    time_to_metro_min: number | null;
    min_price: number | null;
    menu_image: string | null;
    slug: string;
    has_prefix_level: boolean;
    link?: string;
};

type Commercial = {
    metro: Metro;
    name: string;
    time_to_metro_min: number | null;
    min_price: number;
    menu_image: string;
    slug: string;
    has_prefix_level: boolean;
    link?: string;
};

type DefaultItem = {
    title?: string;
    name?: string;
    order?: number;
    link?: string;
    url?: string;
    column?: number;
    footer_only?: boolean;
};

type SocialNetwork = {
    name: string;
    icon: string;
    link: string;
};

type CompanyRule = {
    number_of_rule: number;
    name: string;
    text: string;
    name_label: string;
    menu_description: string | null;
};

type PromoCard = {
    title: string;
    description: string;
    button_link: string;
    button_text: string;
    order: number;
};

type MortgageCard = {
    title: string;
    description: string;
    mortgage_digits: {
        init_payment: number,
        min_monthly_payment: number,
    };
    link: string;
    link_text: string;
    order: number;
}

type MenuHeaderItem = {
    order: number;
    title: string;
    link: string;
    tab: string;
}

type Spec = {
    value: string | number;
    label: string | number;
}

type Favorites = {
    count: number,
    flat: FlatCard[] | [],
    commercial: FlatCard[] | [],
    pantry: FlatCard[] | [],
    parking: FlatCard[] | [],
}

export type {
    Metro,
    Project,
    DefaultItem,
    Commercial,
    SocialNetwork,
    CompanyRule,
    PromoCard,
    MortgageCard,
    Spec,
    MenuHeaderItem,
    Favorites,
};
