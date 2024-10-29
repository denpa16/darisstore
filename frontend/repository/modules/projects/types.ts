import type { FacetsType } from '~/types/filter';

export interface RoomsPrice {
    room: number,
    price: number,
}

export interface IProjectCardGallery {
    id: string,
    image: string,
}

export interface IProjectCardAdvaGallery {
    title: string,
    description: string,
    image: string,
}

export interface IProjectCardEstate {
    count: number,
    min_price: number,
    sale: number,
}

export interface IProjectCardEstateList {
    flats: IProjectCardEstate,
    parking: IProjectCardEstate,
    storage: IProjectCardEstate,
    commercial: IProjectCardEstate,
}

export interface IProjectCardBuildingsCompletion {
    number: number,
    completion_quarter: number,
    completion_year: number,
    percent: number
}

export interface IProjectCard {
    id: number,
    name: string,
    slug: string,
    address: string,
    complete_date: string,
    min_price: number,
    image: string,
    coords: string,
    flats_count: number,
    tags: string[]
    metro_set: [
        {
            walk_time: number,
            car_time: number,
            metro_name: string,
        }
    ]
    completion_year: number,
    completion_quarter: number,
    buildings_completion: IProjectCardBuildingsCompletion[],
    gallery: IProjectCardGallery[],
    adva_gallery: IProjectCardAdvaGallery[],
    estate_list: IProjectCardEstateList,
}

export interface ProjectFacets extends FacetsType {
    rooms: number[],
    transformer: boolean[],
    has_discount: boolean[],
    price: {
        min: number,
        max: number,
    },
    ppm: {
        min: number,
        max: number,
    },
    renovation: Array<number | null>,
    area: {
        min: number,
        max: number,
    },
    project: Array<string | null>,
    metro: number[],
    district: Array<number | null>,
    building: string[],
    floor: {
        min: number,
        max: number,
    },
    has_view: number[],
    completion: Array<string | null>,
    completion_before: {
        min: string,
        max: string,
    },
    window_views: number[],
    sides: number[],
    has_lodge: boolean[],
    has_separate_entrance: boolean[],
    is_remarkable: boolean[],
    has_mollywindow: boolean[],
    has_master_bedroom: boolean[],
    is_tripartite: boolean[],
    is_premium: boolean[],
    rare_formats: string[],
    balcony_type: number[],
    metro_time: number[],
    sales_start: number[],
    remarkable: boolean[],
    category: string[],
    views: boolean[],
    alter_room: string[],
    category_class: number[],
    realized_project: number[],
    windows_directions: string[],
    has_laundry_room: boolean[],
    has_alcove_for_bed: boolean[],
    has_dressing_room: boolean[],
    type: string[],
}

export interface IProjectsCardsResponse {
    count: number,
    results: IProjectCard,
}

export interface IProjectsFacetsResponse {
    facets: ProjectFacets,
    count: number,
    projects_count: number,
}
