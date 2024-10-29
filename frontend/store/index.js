import { defineStore } from 'pinia';
import { useDeviceStore } from '@idaproject/core/store/device';
import { useDomainStore } from '@idaproject/core/store/domain';

export const useMainStore = defineStore('main', () => {
    async function nuxtServerInit() {
        try {
            await Promise.all([
                useDeviceStore()
                    .init(),
                useDomainStore()
                    .init(),
                useDeviceStore()
                    .setIsRefYandexState(),
            ]);
        } catch (e) {
            console.error('[nuxtServerInit]: ', e);
        }
    }

    return {
        nuxtServerInit,
    };
});
