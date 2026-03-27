/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class AvailabilityWidget extends Component {
    static template = "library_book.AvailabilityWidget";
    static props = {
        ...standardFieldProps,
    };

    get isAvailable() {
        return this.props.record.data[this.props.name];
    }
}

registry.category("fields").add("availability_widget", {
    component: AvailabilityWidget,
    supportedTypes: ["boolean"],
});