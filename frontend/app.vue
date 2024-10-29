<script lang="ts"
        setup
>
const route = useRoute();
const routePath: string = route?.matched[0].path;
const config = useRuntimeConfig();

useRouteCache(helper => {
    if (routePath !== '/:slug(.*)*' && !config.public.DISABLE_ROUTE_CACHE) {
        helper
            .setCacheable()
            .setMaxAge(400);
    } else {
        helper.setUncacheable();
    }
});
</script>

<template>
    <div>
        <NuxtLayout>
            <NuxtPage />
        </NuxtLayout>
    </div>
</template>
