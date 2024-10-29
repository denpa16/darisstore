// Json
import * as flatsData from '~/assets/mock/json/allFlats.json';
import { handleFlatsSpecsFacets } from '@/assets/mock/ts/mock-utils';

export default defineEventHandler(event => {
    // Вся недвижимость, для фильтрации
    const [...allFlats] = flatsData.allFlats;

    const query = getQuery(event);

    const skipParams = ['zone', 'propertyType'];
    const specs = handleFlatsSpecsFacets(allFlats, query || {}, skipParams);
    return specs;
});
