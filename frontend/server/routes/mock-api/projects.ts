// Json
import * as projectsData from '~/assets/mock/json/projects.json';
import * as flatsData from '~/assets/mock/json/allFlats.json';
import { handleFlatsFilter } from '@/assets/mock/ts/mock-utils';

export default defineEventHandler(event => {
    // Получаем из json все проекты
    const [...projects] = projectsData.projects;

    // Вся недвижимость, для фильтрации
    const [...allFlats] = flatsData.allFlats;


    const query = getQuery(event);

    // Временно удаляются лишние свойства
    delete query.limit;
    delete query.offset;

    const filteredItems = query ? handleFlatsFilter(allFlats, query) : allFlats;
    const projectsArr = [...new Set(filteredItems.map((i: Record<string, string | number>) => i.project))];
    const results = projects.filter(i => projectsArr.includes(i.slug));
    return { count: results?.length, results };
});
