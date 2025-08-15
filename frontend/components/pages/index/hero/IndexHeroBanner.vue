<template>
    <div :class="$style.IndexHeroBanner">
        <div class="container">
            <div ref="marquee" :class="$style.list">
                <div
                    v-for="t in texts"
                    ref="texts"
                    :key="`text_${t}`"
                    :class="$style.text"
                    v-html="t"
                />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'IndexHeroBanner',

    data() {
        return {
            texts: [
                'Федерация кикбоксинга России',
                'Федерация кикбоксинга Московской области',
                'Спортобщество бокса России',
                'Мособлспорт',
            ],

            position: 0,
            speed: 1,
            animationFrame: null, // ID текущего `requestAnimationFrame`
        };
    },

    mounted() {
        const marquee = this.$refs.marquee;
        if (marquee) {
            const clone = marquee.cloneNode(true);
            marquee.appendChild(clone);

            this.startMarquee(marquee);
        }
    },

    beforeDestroy() {
        cancelAnimationFrame(this.animationFrame);
    },

    methods: {
        startMarquee(marquee) {
            const animate = () => {
                this.position -= this.speed;
                if (Math.abs(this.position) >= marquee.scrollWidth / 2) {
                    this.position = 0;
                }
                marquee.style.transform = `translateX(${this.position}px)`;

                this.animationFrame = requestAnimationFrame(animate);
            };

            this.animationFrame = requestAnimationFrame(animate);
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .IndexHeroBanner {
        overflow: hidden;
        padding: 3.2rem 0;
        background: $primary-700;

        @include respond-to(mobile) {
            padding: 1.6rem 0;
        }
    }

    .list {
        display: flex;
        align-items: center;
        gap: 8rem;
        width: 100%;
    }

    @keyframes run {
        from {
            transform: translateX(0);
        }

        to {
            transform: translateX(-100%);
        }
    }

    .text {
        @include text(h5);

        white-space: nowrap;
        color: $white;

        @include respond-to(mobile) {
            @include text(m12);
        }
    }
</style>
