import HttpFactory from '@/repository/factory.ts';

class FormsMockModule extends HttpFactory {
    async sendContactForm(formData: FormData, options: object): Promise<object> {
        return this.call<object>('POST', '/mock-api/request/', { body: formData, ...options });
    }
}

export default FormsMockModule;
