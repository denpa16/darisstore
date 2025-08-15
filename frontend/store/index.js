export const state = () => ({});

export const getters = {};

export const actions = {
    async nuxtServerInit({ dispatch }, context) {
        try {
            await Promise.all([
                dispatch('domain/init', context),
            ]);
        } catch (e) {
            console.error('[nuxtServerInit]: ', e);
        }
    },
};

export const mutations = {};
