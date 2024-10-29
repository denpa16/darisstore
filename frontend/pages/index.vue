<script setup lang="ts">
import VModal from '@/components/layout/VModal.vue';
import ContactModal from '@/components/modals/ContactModal.vue';

// Pinia
import { useDomainStore } from '@idaproject/core/store/domain';
import { useDeviceStore } from '@idaproject/core/store/device';
// #endregion

// #region Data
const domainStore = useDomainStore();
const deviceStore = useDeviceStore();

const showModal = ref<boolean>(false);
// #endregion
</script>

<template>
    <div :class="['page', $style.MainPage]">
        <div :class="['container', $style.container]">
            <div :class="$style.logos">
                <VIcon
                    :class="$style.logoIda"
                    name="ida-front"
                    size="custom"
                />

                <span>+</span>

                <VIcon
                    name="nuxt"
                    :class="$style.logoNuxt"
                    size="custom"
                />
            </div>

            <div :class="['styled-content', $style.content]">
                <h1>Nuxt Template</h1>

                <h2>Domain/Proxy:</h2>

                <ul>
                    <li>{{ domainStore.getSiteDomain }}</li>
                </ul>


                <h2>Device info:</h2>

                <ul :class="$style.list">
                    <li>
                        <span>
                            Webp supported:
                            <VIcon
                                :class="[$style.check, {'_green': deviceStore.isWebpSupported}]"
                                :name="deviceStore.isWebpSupported ? 'check' : 'close'"
                                size="xs"
                            />
                        </span>
                    </li>

                    <li>
                        <span>
                            Mac iOS:
                            <VIcon
                                :class="[$style.check, {'_green': deviceStore.isIos}]"
                                :name="deviceStore.isIos ? 'check' : 'close'"
                                size="xs"
                            />
                        </span>
                    </li>

                    <li>
                        <span>
                            Mac OSX:
                            <VIcon
                                :class="[$style.check, {'_green': deviceStore.isOsx}]"
                                :name="deviceStore.isOsx ? 'check' : 'close'"
                                size="xs"
                            />
                        </span>
                    </li>

                    <li>
                        <span>
                            Safari:
                            <VIcon
                                :class="[$style.check, {'_green': deviceStore.isSafari}]"
                                :name="deviceStore.isSafari ? 'check' : 'close'"
                                size="xs"
                            />
                        </span>
                    </li>

                    <li>
                        <transition
                            name="fade-fast"
                            mode="out-in"
                        >
                            <span :key="`touch_${deviceStore.isIpadPro}`">
                                iPad Pro (client-only):
                                <VIcon
                                    :class="[$style.check, {'_green': deviceStore.isIpadPro}]"
                                    :name=" deviceStore.isIpadPro ? 'check' : 'close'"
                                    size="xs"
                                />
                            </span>
                        </transition>
                    </li>

                    <li>
                        <span>
                            Hydration status:&nbsp;
                            <HydrationStatus />
                        </span>
                    </li>
                </ul>
            </div>

            <button
                :class="$style.modalBtn"
                @click="showModal = true"
            >

                Open modal
            </button>

            <VModal v-model="showModal">
                <ContactModal @close="showModal = false" />
            </VModal>
        </div>
    </div>
</template>

<style lang="scss"
       module
>
    .MainPage {
        display: flex;
        height: 100%;
        min-height: 100vh;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .logos {
        display: flex;
        align-items: center;
        flex-flow: nowrap row;

        svg {
            shape-rendering: geometricprecision;
        }

        span {
            font-size: 3rem;
            color: $base-900;
        }
    }

    .logoNuxt {
        width: 11rem;
        height: 8rem;
    }

    .logoIda {
        width: 22rem;
        height: 8rem;
        color: $primary-600;
    }

    .list {
        span {
            display: inline-flex;
            align-items: center;
            white-space: nowrap;
            line-height: 1.2;
            letter-spacing: -.005em;
            transition: color $default-transition;
        }

        .check {
            width: 1em;
            height: 1em;
            margin-left: .6rem;
            padding: 2px 0;
            vertical-align: baseline;
            color: $base-900;

            &:global(._green) {
                padding: 0;
                color: $base-500;
            }
        }
    }

    .modalBtn {
        margin-top: 2rem;
        padding: 1.2rem;
        border-radius: 1rem;
        background: #e4e4e4;
        font-size: 1.2rem;
        transition: opacity .3s;
        cursor: pointer;
        user-select: none;

        &:hover {
            opacity: .7;
        }
    }
</style>
