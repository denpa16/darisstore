import VDatePicker from 'v-calendar';
import 'v-calendar/dist/style.css';

export default defineNuxtPlugin(({ vueApp }) => {
    vueApp.use(VDatePicker);
});
