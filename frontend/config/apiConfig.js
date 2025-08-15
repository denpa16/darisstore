import mainPageApi from '~/config/api/mainPage';
import publicationsApi from '~/config/api/publications.js';
import requestApi from '~/config/api/request.js';

const apiConfig = {
    ...mainPageApi,
    ...publicationsApi,
    ...requestApi,
};

export default apiConfig;
