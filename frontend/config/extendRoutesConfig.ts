import type { NuxtPage } from 'nuxt/schema';
import expertiseRoutes from './extend-routes/expertiseRoutes.ts';

export default (nuxtPages: NuxtPage[], rootFolder: string) => {
    expertiseRoutes(nuxtPages, rootFolder);
};
