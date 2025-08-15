<template>
    <header id="header" :class="$style.TheHeader">
        <transition name="dropdown" mode="out-in">
            <div
                v-if="promo"
                key="promo"
                :class="$style.promo"
                @click="handleClickPromo"
            >
                <div :class="[$style.promoWrapper, 'container']">
                    <button :class="$style.promoClose" @click.stop="handleClosePromo">
                        <VIcon size="xsmall" name="close"/>
                    </button>

                    <div
                        v-if="promo?.header_promo_title"
                        :class="$style.promoTitle"
                        v-html="promo.header_promo_title"
                    />

                    <button :class="$style.promoLink">
                        <VIcon size="xsmall" name="arrow-right"/>
                    </button>
                </div>
            </div>
        </transition>

        <div :class="[$style.wrapper, 'container']">
            <NuxtLink to="/">
                <LogoIcon
                    :class="$style.logo"
                    name="logo"
                    size="custom"
                />
            </NuxtLink>

            <div :class="$style.links">
                <button
                    v-for="item in menuItems"
                    :key="`btn_${item?.value}_${item?.href}`"
                    :class="[$style.link, {[$style._active]: item.value === activeItem || activeItem.includes(item.href)}]"
                    @click="handleClick(item)"
                >
                    {{ item.label }}
                </button>
            </div>

            <div :class="$style.rightSide">
                <button :class="$style.btn" @click="handleRequest">Написать нам</button>

                <a :class="$style.phone" :href="`tel:${phone}`">
                    <VIcon
                        :class="$style.icon"
                        size="xsmall"
                        name="phone"
                    />
                    {{ phone }}
                </a>
            </div>

            <transition name="fade-fast" mode="out-in">
                <VButton
                    :key="String(isModalOpen)"
                    size="custom"
                    color="transparent"
                    tag="button"
                    @click="onModalButtonClick"
                >
                    <VIcon
                        :class="$style.menuButton"
                        :name="isModalOpen ? 'close' : 'burger'"
                        size="small"
                    />
                </VButton>
            </transition>
        </div>
    </header>
</template>

<script>
// Vuex
import { mapActions, mapGetters, mapState } from 'vuex';

// Utils
import { scrollTo } from '~/assets/js/utils/common-utils.js';

// Constants
import { PHONE_NUMBER } from '~/assets/js/constants/index.js';

// Components
import VButton from '~/components/ui/button/VButton.vue';
import LogoIcon from '~/components/icons/LogoIcon.vue';
import VIcon from '~/components/ui/icon/VIcon.vue';
import { FORM_TYPES } from '~/assets/js/constants/forms.js';

export default {
    name: 'TheHeader',
    components: { VIcon, LogoIcon, VButton },

    data() {
        return {
            isModalOpen: false,
            phone: PHONE_NUMBER,
            anchors: [],
            promo: null,
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

    mounted() {
        this.fetchPromo();
    },

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
            changeHasPromo: 'menu/changeHasPromo',
        }),

        async fetchPromo() {
            try {
                const promo = await this.$axios.$get(this.$api.mainPage.promo);

                if (promo) {
                    this.promo = promo;

                    this.changeHasPromo(true);
                }
            } catch (err) {
                console.warn('[TheHeader/asyncData] request failed: ', err);
            }
        },

        handleClosePromo() {
            this.promo = null;
            this.changeHasPromo(false);
        },

        handleClickPromo() {
            if (this.promo?.header_promo_link) {
                window.open(this.promo.header_promo_link, '_blank');
            }
        },

        handleClick(val) {
            if (val?.href) {
                this.$router.push({
                    path: val.href,
                });
            } else if (this.$route.path.includes('/news')) {
                this.$router.push({
                    path: '/',
                    hash: val.value,
                });
            } else {
                scrollTo(val.value);
            }
            this.changeActiveItem(val?.href ?? val?.value);
        },

        onChange(slug) {
            setTimeout(() => this.handleClick(slug), 550);
        },

        onModalButtonClick() {
            if (this.isModalOpen) {
                this.$modal.event.$off('change', this.onChange);
                this.$modal.close();
                return;
            }

            this.isModalOpen = true;

            this.$modal.open(() => import('@/components/layout/modals/menu/MenuModal.vue'), {
                position: 'top',
                isShowHeader: true,
                items: this.menuItems,
            }, () => {
                setTimeout(() => this.isModalOpen = false, 0);
            });

            this.$modal.event.$on('change', this.onChange);
        },

        handleRequest() {
            this.$modal.open(() => import('@/components/layout/modals/FormModal.vue'), {
                position: 'right',
                type: FORM_TYPES.toWork,
            });
        },
    },
};
</script>

<style lang="scss" module>
    .TheHeader {
        position: sticky;
        top: 0;
        left: 0;
        z-index: $header-z-index;
        width: 100%;
        border-bottom: 1px solid $base-150;
        background: $white;

        @include respond-to(tablet) {
            min-height: $header-h-mobile;
        }

        .menuButton {
            display: none;

            @include respond-to(tablet) {
                display: block;
            }
        }
    }

    .promo {
        display: flex;
        align-items: center;
        height: 4.4rem;
        background: $primary-500;
        transition: $default-transition;
        cursor: pointer;
        user-select: none;

        @include hover {
            background: $primary-700;

            .promoLink {
                transform: translateX(1rem);
            }
        }

        @include respond-to(tablet) {
            height: 4rem;
        }
    }

    .promoWrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.6rem;
        width: 100%;
    }

    .promoTitle {
        @include text(s16);

        overflow: hidden;
        width: 100%;
        text-align: center;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-weight: 400;
        color: $white;

        @include respond-to(tablet) {
            @include text(m14);
        }
    }

    .promoClose,
    .promoLink {
        display: flex;
        align-items: center;
        justify-content: center;
        color: $white;
        transform-origin: center;
        transition: $default-transition;
        cursor: pointer;
        user-select: none;
    }

    .promoClose {
        @include hover {
            transform: rotate(180deg);
        }
    }

    .wrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 4rem;
        height: $header-h;

        @include respond-to(tablet) {
            gap: 4rem;
            height: $header-h-mobile;
        }
    }

    .logo {
        width: 6rem;
        height: 4rem;
        transition: opacity $default-transition;

        @include respond-to(tablet) {
            height: 3.2rem;
        }

        @include hover {
            opacity: .7;
        }
    }

    .links {
        display: flex;
        align-items: center;
        flex-grow: 1;
        gap: 4rem;
        height: 100%;

        @include respond-to(tablet) {
            display: none;
        }
    }

    .link {
        @include text(m16);

        position: relative;
        display: flex;
        align-items: center;
        height: 100%;
        transition: color $default-transition;
        cursor: pointer;

        &:after {
            content: "";
            position: absolute;
            bottom: -1px;
            left: 50%;
            z-index: 1;
            display: flex;
            width: 100%;
            height: 2px;
            background: $primary-500;
            transform: translateX(-50%) scaleX(0);
            transition: transform $default-transition;
        }

        &._active {
            color: $primary-500;

            &:after {
                transform: translateX(-50%) scaleX(1);
            }
        }

        @include hover {
            color: $primary-500;
        }
    }

    .rightSide {
        display: flex;
        align-items: center;
        gap: 3.2rem;
    }

    .btn {
        @include text(m16);

        transition: color $default-transition;
        cursor: pointer;

        @include hover {
            color: $primary-500;
        }

        @include respond-to(tablet) {
            display: none;
        }
    }

    .phone {
        @include text(m16);

        display: flex;
        align-items: center;
        gap: .8rem;

        @include respond-to(tablet) {
            @include text(h5);

            color: $base-700;
        }
    }

    .icon {
        @include respond-to(tablet) {
            display: none;
        }
    }
</style>
