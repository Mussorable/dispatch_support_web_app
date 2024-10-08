import Transport from './Transport.js';

export default class Trucks extends Transport {
    constructor(transport_type_api = '/trucks', transport_title = 'Trucks') {
        super(transport_type_api, transport_title);
    }
}