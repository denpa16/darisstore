import { $fetch, type FetchOptions } from 'ofetch';
import { defineNuxtPlugin } from '#app';
import ProjectsMockModule from '~/repository/modules/projects/projects-mock';
import FormsMockModule from '@/repository/modules/forms/forms.ts';

/** ApiInstance interface provides us with good typing */
interface IApiInstance {
    projectsMock: ProjectsMockModule;
    formsMock: FormsMockModule;
}

export default defineNuxtPlugin(nuxtApp => {
    let endpoint;

    if (import.meta.server) {
        if (nuxtApp.$config.PROXY_URL) {
            endpoint = nuxtApp.$config.PROXY_URL;
        // } else if (nuxtApp.$config.SERVER_API_URL) {
        //     endpoint = nuxtApp.$config.SERVER_API_URL;
        } else {
            endpoint = 'http://backend:8000/';
        }
    } else {
        endpoint = `${location.origin}/`;
    }

    // const { csrf } = useCsrf();

    const fetchOptions: FetchOptions = {
        baseURL: endpoint,
        // headers: { 'X-CSRFToken': csrf },
    };

    /** create a new instance of $fetcher with custom option */
    const apiFetcher = $fetch.create(fetchOptions);

    /** an object containing all repositories we need to expose */
    const modules: IApiInstance = {
        projectsMock: new ProjectsMockModule(apiFetcher),
        formsMock: new FormsMockModule(apiFetcher),
    };

    return {
        provide: {
            fetchData: modules,
        },
    };
});
