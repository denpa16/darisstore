<template>
    <ul :class="$style.IndexMissionCards">
        <li
            v-for="card in cards"
            :key="`card_${card.icon}`"
            :class="$style.card"
        >
            <div :class="$style.iconWrap">
                <VIcon
                    size="small"
                    :class="$style.icon"
                    :name="card.icon"
                />
            </div>

            <div :class="$style.title" v-html="card.title"/>
            <div :class="$style.description" v-html="card.description"/>
        </li>
        <li
            key="card_btn"
            :class="[$style.card, $style._btnWrap]"
            @click="handleRequest"
        >
            <VIconButton
                color="secondary"
                size="small"
                icon="arrow-right"
            />

            <div :class="$style.description" >Написать нам</div>
        </li>
    </ul>
</template>

<script>
export default {
    name: 'IndexMissionCards',

    data() {
        return {
            cards: [
                {
                    icon: 'calendar',
                    title: '2016',
                    description: 'основание школы',
                },
                {
                    icon: 'people',
                    title: '120+',
                    description: 'спортсменов',
                },
                {
                    icon: 'boxing',
                    title: '10+ лет',
                    description: 'стаж работы тренеров',
                },
            ],
        };
    },

    methods: {
        handleRequest() {
            this.$modal.open(() => import('@/components/layout/modals/FormModal.vue'), {
                position: 'right',
            });
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .IndexMissionCards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.6rem;

        @include respond-to(mobile) {
            grid-template-columns: repeat(2, 1fr);
            gap: 1.2rem;
        }
    }

    .card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 2rem;
        border-radius: 1.2rem;
        background: $base-150;

        &._btnWrap {
            display: none;
            background: $primary-500;

            .description {
                color: $white;
            }

            @include respond-to(mobile) {
                display: flex;
            }
        }
    }

    .iconWrap {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 4rem;
        aspect-ratio: 1;
        border-radius: .8rem;
        background: $white;
    }

    .icon {
        color: $primary-500;
    }

    .title {
        @include text(h3);

        margin: 3.2rem 0 .4rem;
        color: $primary-500;

        @include respond-to(mobile) {
            @include text(h4);
        }
    }

    .description {
        @include text(r14);

        color: $base-500;
    }
</style>
