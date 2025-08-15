<template>
    <section :class="$style.Error">
        <div
            :class="$style.wrap"
            class="container"
        >
            <h1
                :class="$style.title"
                v-html="content.status"
            />
            <div
                :class="$style.text"
                v-html="content.text"
            />
            <VButton
                v-if="content.btnText"
                @click="content.btnAction"
            >
                {{ content.btnText }}
            </VButton>
        </div>
    </section>
</template>

<script>
import VButton from '~/components/ui/button/VButton.vue';

export default {
    components: { VButton },
    layout: 'errorLayout',

    props: {
        error: {
            type: Object,
            default: () => ({}),
        },
    },

    computed: {
        content() {
            const content404 = {
                status: '404',
                text: 'Этой страницы ещё не существует, или мы не успели ее построить',
                btnText: 'На главную',
                btnAction: this.toMainPage,
            };

            const content500 = {
                status: '500',
                text: 'Возникла ошибка на стороне сервера. Ничего страшного, просто перезагрузите страницу',
                btnText: 'Перезагрузить страницу',
                btnAction: this.pageReload,
            };

            const content502 = {
                status: '502',
                text: 'Вероятно сервер перегружен. Ничего страшного, просто перезагрузите страницу',
                btnText: 'Перезагрузить страницу',
                btnAction: this.pageReload,
            };

            const contentTech = {
                status: 'тех. работы',
                text: 'Мы улучшаем наш сайт',
            };

            switch (this.error.statusCode) {
                case 404:
                    return content404;
                case 502:
                    return content502;
                case 500:
                    return content500;
                default:
                    return contentTech;
            }
        },
    },

    methods: {
        toMainPage() {
            this.$router.push({
                path: '/',
            });
        },

        pageReload() {
            window.location.reload();
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .Error {
        width: 100%;
        height: 100%;
    }

    .wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4rem;
        width: 100%;
        height: 100%;
    }

    .title {
        @include text(h1);
    }

    .text {
        @include text(m18);
    }
</style>
