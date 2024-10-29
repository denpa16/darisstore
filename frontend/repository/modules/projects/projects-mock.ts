import { objectToQuery } from '@idaproject/core/assets/js/utils/query-utils';
import HttpFactory from '~/repository/factory';
import type {
    IProjectsCardsResponse,
    IProjectsFacetsResponse,
} from '~/repository/modules/projects/types';
import type { ServerSpec } from '~/types/filter';

class ProjectsMockModule extends HttpFactory {
    async getResults(values = {}, data = {}): Promise<IProjectsCardsResponse> {
        const $res: IProjectsCardsResponse = await this.call<IProjectsCardsResponse>('GET', `/mock-api/projects/?${objectToQuery(values)}`, data);
        return $res;
    }

    async getSpecs(values = {}, data = {}): Promise<ServerSpec[]> {
        const $res: ServerSpec[] = await this.call<ServerSpec[]>('GET', `/mock-api/projects/specs/?${objectToQuery(values)}`, data);
        return $res || [];
    }

    async getFacets(values = {}, data = {}): Promise<IProjectsFacetsResponse> {
        const $res: IProjectsFacetsResponse = await this.call<IProjectsFacetsResponse>('GET', `/mock-api/projects/facets/?${objectToQuery(values)}`, data);
        return $res;
    }

    // todo добавить тип project
    async getProject(slug = {}, data = {}): Promise<object> {
        const $res: object = await this.call<object>('GET', `/mock-api/projects/${slug}`, data);
        return $res;
    }

    async getBuildings(slug = {}, values = {}, data = {}): Promise<object> {
        const $res: object = await this.call<object>('GET', `/mock-api/projects/${slug}/buildings?${objectToQuery(values)}`, data);
        return $res;
    }

    async getSections(id = {}, values = {}, data = {}): Promise<object> {
        const $res: object = await this.call<object>('GET', `/mock-api/buildings/${id}/sections?${objectToQuery(values)}`, data);
        return $res;
    }

    async getFloors(id = {}, values = {}, data = {}): Promise<object> {
        const $res: object = await this.call<object>('GET', `/mock-api/sections/${id}/floors?${objectToQuery(values)}`, data);
        return $res;
    }

    async getFlats(id = {}, values = {}, data = {}): Promise<object> {
        const $res: object = await this.call<object>('GET', `/mock-api/floors/${id}/flats?${objectToQuery(values)}`, data);
        return $res;
    }
}

export default ProjectsMockModule;
