/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class LibraryDashboard extends Component {
    setup() {
        this.orm = useService("orm");

        this.state = useState({
            counter: 0,
            loading: true,
            filter: "all", // all | available | unavailable
            stats: {
                total_books: 0,
                available_books: 0,
                unavailable_books: 0,
            },
            books: [],
        });

        onWillStart(async () => {
            await this.loadAll();
        });
    }

    async loadAll() {
        await this.loadStats();
        await this.loadBooks();
        this.state.loading = false;
    }

    getDomainFromFilter() {
        if (this.state.filter === "available") {
            return [["is_available", "=", true]];
        }
        if (this.state.filter === "unavailable") {
            return [["is_available", "=", false]];
        }
        return [];
    }

    increment() {
        this.state.counter++;
    }

    async loadStats() {
        const total = await this.orm.searchCount("library.book", []);
        const available = await this.orm.searchCount("library.book", [
            ["is_available", "=", true],
        ]);
        const unavailable = total - available;

        this.state.stats.total_books = total;
        this.state.stats.available_books = available;
        this.state.stats.unavailable_books = unavailable;
    }

    async loadBooks() {
        const domain = this.getDomainFromFilter();
        const records = await this.orm.searchRead(
            "library.book",
            domain,
            ["name", "author", "is_available", "category_id"],
            { limit: 20 }
        );

        // searchRead retourne un tableau d'objets {id, name, ...}
        this.state.books = records;
    }

    async onFilterChange(ev) {
        this.state.loading = true;
        this.state.filter = ev.target.value; // "all" | "available" | "unavailable"
        await this.loadBooks();
        this.state.loading = false;
    }
}

LibraryDashboard.template = "library_book.LibraryDashboard";
registry.category("actions").add("library_book.dashboard_action", LibraryDashboard);