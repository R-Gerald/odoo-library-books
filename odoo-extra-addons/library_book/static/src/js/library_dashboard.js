/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class LibraryDashboard extends Component {
    setup() {
        this.orm = useService("orm");

        this.state = useState({
            counter: 0,
            stats: {
                total_books: 0,
                available_books: 0,
                unavailable_books: 0,
            },
            loading: true,
        });

        // onWillStart est appelé avant le premier rendu du composant
        onWillStart(async () => {
            await this.loadStats();
        });
    }

    increment() {
        this.state.counter++;
    }

    async loadStats() {
        // Appel RPC vers le backend Odoo
        const total = await this.orm.searchCount("library.book", []);
        const available = await this.orm.searchCount("library.book", [
            ["is_available", "=", true],
        ]);
        const unavailable = total - available;

        this.state.stats.total_books = total;
        this.state.stats.available_books = available;
        this.state.stats.unavailable_books = unavailable;
        this.state.loading = false;
    }
}

// Lier au template XML
LibraryDashboard.template = "library_book.LibraryDashboard";

// Enregistrer comme "client action"
registry.category("actions").add("library_book.dashboard_action", LibraryDashboard);