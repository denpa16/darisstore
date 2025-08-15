<template>
    <footer
        id="footer"
        :class="$style.TheFooter"
    >
        <div :class="[$style.main, 'container']">
            <div :class="$style.logoWrapper">
                <LogoIcon
                    :class="$style.logo"
                    @click.native="scrollTo"
                />

                <div>
                    <p>© 2016 - 2025 СК ШАГ</p>

                    <a
                        :class="$style.phone"
                        :href="`tel:${phone}`"
                    >
                        {{ phone }}
                    </a>
                </div>

                <div>
                    <p>Мы в социальных сетях</p>

                    <div :class="$style.buttons">
                        <VIconButton
                            tag="a"
                            :href="telegramLink"
                            target="_blank"
                            icon="telegram"
                            :size="$deviceIs.mobile ? 'small' : 'large'"
                            color="secondary"
                        />

                        <VIconButton
                            tag="a"
                            :href="whatsappLink"
                            target="_blank"
                            icon="whatsapp"
                            :size="$deviceIs.mobile ? 'small' : 'large'"
                            color="secondary"
                        />

                        <VIconButton
                            tag="a"
                            :href="vkLink"
                            target="_blank"
                            icon="vk"
                            :size="$deviceIs.mobile ? 'small' : 'large'"
                            color="secondary"
                        />
                    </div>
                </div>
            </div>

            <div :class="$style.questions">
                <div :class="$style.questionsTitle">
                    Ответим
                    <br>
                    на ваши вопросы
                </div>
                <VButton
                    :class="$style.questionsBtn"
                    :size="$deviceIs.mobile ? 'small' : 'medium'"
                    @click="handleRequest"
                >
                    Написать нам
                </VButton>
            </div>

            <nav :class="$style.nav">
                <div :class="$style.columnTitle">Навигация</div>
                <VLink
                    v-for="item in menuItems"
                    :key="item.value"
                    :class="[$style.link, {[$style._active]: item.value === activeItem || activeItem.includes(item.href)}]"
                    @click="scrollTo(item.value)"
                >
                    {{ item.label }}
                </VLink>
            </nav>

            <div :class="$style.branches">
                <div :class="$style.columnTitle">Залы</div>

                <p :class="$style.branchSubtitle">Адрес:</p>
                <ul :class="$style.branchList">
                    <li
                        v-for="(item, ind) in branches"
                        :key="`branch_${ind}`"
                        :class="$style.branch"
                    >
                        <a
                            :class="$style.branchLink"
                            target="_blank"
                            :href="item.value"
                        >
                            {{ item.address }}
                        </a>
                    </li>
                </ul>

                <p :class="$style.branchSubtitle">График работы</p>
                <div :class="$style.branch">
                    Ежедневно 08:00 — 22:00
                </div>
            </div>
        </div>

        <div :class="[$style.plank, 'container']">
            <p :class="$style.disclaimer">
                Любая информация, представленная на данном сайте, носит исключительно
                информационный характер, не является офертой, определяемой положениями ст.437 ГК РФ.
            </p>

            <a
                :class="$style.privacy"
                :href="policyLink"
                target="_blank"
            >
                Политика конфиденциальности
            </a>
        </div>
    </footer>
</template>

<script>
// Vuex
import { mapGetters, mapState } from 'vuex';

// Utils
import { scrollTo } from '~/assets/js/utils/common-utils.js';

// Constants
import {
    PHONE_NUMBER,
    POLICY_LINK,
    TELEGRAM_LINK, VK_LINK,
    WHATSAPP_LINK,
} from '~/assets/js/constants/index.js';

// Components
import LogoIcon from '~/components/icons/LogoIcon.vue';
import { branches } from '~/assets/js/constants/branches.js';

export default {
    name: 'TheFooter',
    components: {
        LogoIcon,
    },

    data() {
        return {
            whatsappLink: WHATSAPP_LINK,
            telegramLink: TELEGRAM_LINK,
            vkLink: VK_LINK,
            phone: PHONE_NUMBER,
            policyLink: POLICY_LINK,
            branches: [
                branches.main,
                branches.branch1,
                branches.branch2,
                branches.branch3,
            ],
        };
    },

    computed: {
        ...mapState({
            menuItems: state => state.menu?.menuItems || [],
        }),

        ...mapGetters({
            activeItem: 'menu/getActiveItem',
        }),
    },

    methods: {
        scrollTo,

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
    .TheFooter {
        border-radius: 2.4rem 2.4rem 0 0;
        background-color: $base-150;
    }

    .main {
        display: flex;
        justify-content: space-between;
        padding: 6.4rem;

        @include respond-to(tablet) {
            display: grid;
            grid-template-columns: 2fr 1fr;
            grid-auto-flow: column;
            gap: 3.2rem;
            padding: 3.2rem;
        }

        @include respond-to(mobile) {
            display: flex;
            flex-direction: column;
            gap: 3.2rem;
            padding: 3.2rem 1.6rem;
        }
    }

    .logoWrapper {
        display: flex;
        flex-direction: column;
        gap: 2.4rem;

        p {
            @include text(m14);

            margin-bottom: .8rem;
            color: $base-500;
        }

        @include respond-to(tablet) {
            grid-column: 1/2;
        }

        @include respond-to(mobile) {
            display: grid;
            grid-template-columns: 1fr 6rem;
            gap: 2.4rem 5.4rem;
            order: 1;
        }
    }

    .logo {
        width: 8rem;
        height: 8rem;
        margin-bottom: .8rem;
        transition: opacity $default-transition;
        cursor: pointer;
        user-select: none;

        @include hover {
            opacity: .6;
        }

        @include respond-to(mobile) {
            grid-column: 2/-1;
            grid-row: 1/3;
            width: 6rem;
            height: 6rem;
        }
    }

    .phone {
        @include text(h4);

        color: $primary-500;
        transition: color $default-transition;

        @include hover {
            color: $primary-700;
        }

        @include respond-to(mobile) {
            @include text(h5);
        }
    }

    .questions {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: space-between;

        @include respond-to(tablet) {
            grid-column: 1/2;
        }

        @include respond-to(mobile) {
            order: 3;
        }
    }

    .questionsTitle {
        @include text(h3);

        text-transform: uppercase;
        color: $base-300;

        &:first-line {
            color: $base-900;
        }

        @include respond-to(mobile) {
            @include text(h4);

            margin-bottom: 3.2rem;
        }
    }

    .columnTitle {
        @include text(s20);

        margin-bottom: 1.6rem;
        color: $base-700;
    }

    .branchSubtitle {
        @include text(r14);

        margin-bottom: 1.2rem;
        color: $base-500;
    }

    .branch {
        @include text(m14);

        color: $base-700;
    }

    .branchList {
        display: flex;
        flex-direction: column;
        gap: .8rem;
        margin-bottom: 2.4rem;
    }

    .branches,
    .nav {
        @include text(m16);

        display: flex;
        flex-direction: column;
        color: $base-700;

        @include respond-to(tablet) {
            grid-column: 2/3;
        }
    }

    .nav {
        @include respond-to(mobile) {
            order: 2;
        }
    }

    .branches {
        @include respond-to(mobile) {
            order: 4;
        }
    }

    .branchLink {
        transition: opacity $default-transition;
        cursor: pointer;
        user-select: none;

        @include hover {
            opacity: .6;
        }
    }

    .link {
        height: 3.2rem;
        transition: opacity $default-transition;
        cursor: pointer;
        user-select: none;

        &._active {
            color: $primary-500;

            &:after {
                transform: translateX(-50%) scaleX(1);
            }
        }

        @include hover {
            opacity: .6;
        }
    }

    .plank {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2.8rem;
        padding: 1.6rem 6.4rem;
        border-top: .1rem solid $base-300;

        @include respond-to(tablet) {
            align-items: flex-start;
            flex-direction: column-reverse;
            padding: 2rem 1.6rem 1.6rem;
        }
    }

    .disclaimer {
        @include text(m12);

        max-width: 63.1rem;
        color: $base-500;
    }

    .privacy {
        @include text(m14);

        display: block;
        color: $base-500;
        transition: opacity $default-transition;
        cursor: pointer;
        user-select: none;

        @include hover {
            opacity: .6;
        }
    }

    .buttons {
        display: flex;
        gap: .8rem;
        margin-top: .4rem;
    }
</style>
