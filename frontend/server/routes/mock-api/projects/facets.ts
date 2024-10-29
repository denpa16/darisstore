// Json
import * as flatsData from '~/assets/mock/json/allFlats.json';
import { handleFlatsSpecsFacets } from '@/assets/mock/ts/mock-utils';

export default defineEventHandler(event => {
    // Вся недвижимость, для фильтрации
    const [...allFlats] = flatsData.allFlats;

    const query = getQuery(event);

    const skipParams = ['zone'];
    const facets = handleFlatsSpecsFacets(allFlats, query || {}, skipParams, true);
    return { count: null, facets };
});
