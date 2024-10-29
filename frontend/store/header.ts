import { defineStore } from 'pinia';
import { reactive } from 'vue';
import type { IHeaderState } from '@/types/store/header.ts';

export const useHeaderStore = defineStore('header', function() {
    const state = reactive<IHeaderState>({
        isScrolled: false,
        isVisible: true,
        isTransparent: false,
        isMenuWithHero: false,
        isBurgerMenuVisible: false,
    });

    function setScrolled(val: boolean) {
        state.isScrolled = val;
    }

    function changeVisibility(val: boolean) {
        state.isVisible = val;
    }

    function setTransparent(val: boolean) {
        state.isTransparent = val;
    }

    function changeBurgerMenuState(val: boolean) {
        state.isBurgerMenuVisible = val;
    }

    return {
        ...toRefs(state),
        setScrolled,
        changeVisibility,
        setTransparent,
        changeBurgerMenuState,
    };
});
