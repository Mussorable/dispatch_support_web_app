import Transport from "./Transport.js";

export default class Trailers extends Transport {
    constructor(transport_type_api = '/trailers', transport_title = 'Trailers') {
        super(transport_type_api, transport_title);
    }
}