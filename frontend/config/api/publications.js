const publicationsApi = {
    publications: {
        list: (limit = 16, offset = 0) => `/api/publications/?limit=${limit}&offset=${offset}`,
        slug: slug => `/api/publications/${slug}`,
        similar: slug => `/api/publications/${slug}/similar/`,
        news: '/api/publications/news/',
        newsForMainPage: '/api/publications/news_for_main_page/',
    },
};

export default publicationsApi;
