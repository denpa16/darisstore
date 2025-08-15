export const state = () => ({
    domainUrl: null, // определяется автоматически, не менять
    prodDomain: 'skshag.ru',
});

export const getters = {
    getDomainAddress(state) {
        return `https://${state.domainUrl}`;
    },

    getIsTestStage(state) {
        return state.prodDomain !== state.domainUrl;
    },
};

export const actions = {
    async init({ dispatch, state }, context) {
        if (context?.req?.headers['x-forwarded-host']) {
            dispatch('changeActiveDomain', context.req.headers['x-forwarded-host']);
        } else if (process.env.PROXY_URL) {
            const regex = /.*:\/\/(?:www.)?([^/]+)/g;
            const array = [...process.env.PROXY_URL.matchAll(regex)];
            const found = array.map(m => m[1]);
            const domain = found[0];

            if (domain) {
                dispatch('changeActiveDomain', domain);
            }
        } else {
            console.warn('[store domain/actions/init Error] domain address is not set');
        }
    },

    changeActiveDomain({ commit }, payload) {
        commit('SET_DOMAIN', payload);
    },
};

export const mutations = {
    SET_DOMAIN(state, domain) {
        state.domainUrl = domain;
    },
};
