export const state = () => ({
    menuItems: [
        { label: 'Главная', value: '' },
        { label: 'Преимущества', value: 'advantages' },
        { label: 'Тренеры', value: 'coaches' },
        { label: 'О клубе', value: 'about' },
        { label: 'Новости', href: '/blog/news' },
        { label: 'Контакты', value: 'contacts' },
    ],
    activeItem: '',
    hasPromo: false,
});

export const getters = {
    getActiveItem(state) {
        return state.activeItem;
    },

    getHasPromo(state) {
        return state.hasPromo;
    },
};

export const actions = {
    changeActiveItem({ commit }, payload) {
        commit('SET_ACTIVE_ITEM', payload);
    },

    changeHasPromo({ commit }, payload) {
        commit('SET_HAS_PROMO', payload);
    },
};

export const mutations = {
    SET_ACTIVE_ITEM(state, domain) {
        state.activeItem = domain;
    },

    SET_HAS_PROMO(state, payload) {
        state.hasPromo = payload;
    },
};
