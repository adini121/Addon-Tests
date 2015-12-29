#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert
from pages.desktop.home import Home


class TestExtensions:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Featured")

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_top_rated(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by("Top Rated")
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Top Rated")
        Assert.contains("sort=rating", featured_extensions_page.get_url_current_page())

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_most_user(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')

        Assert.contains("sort=users", featured_extensions_page.get_url_current_page())
        user_counts = [extension.user_count for extension in featured_extensions_page.extensions]
        Assert.is_sorted_descending(user_counts)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extensions_are_sorted_by_up_and_coming(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sorter.sort_by('up and coming')
        Assert.equal(featured_extensions_page.sorter.sorted_by, "Up & Coming")
        Assert.contains("sort=hotness", featured_extensions_page.get_url_current_page())
        Assert.greater(len(featured_extensions_page.extensions), 0)

    @pytest.mark.nondestructive
    def test_that_extensions_page_contains_addons_and_the_pagination_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        # Assert that at least one addon is displayed
        Assert.greater(len(featured_extensions_page.extensions), 0)

        if len(featured_extensions_page.extensions) < 20:
            # Assert that the paginator is not present if fewer than 20 extensions are displayed
            Assert.false(featured_extensions_page.is_paginator_present)
        else:
            # Assert that the paginator is present if 20 extensions are displayed
            Assert.true(featured_extensions_page.is_paginator_present)
            Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)
            Assert.false(featured_extensions_page.paginator.is_next_page_disabled)

            featured_extensions_page.paginator.click_next_page()

            Assert.false(featured_extensions_page.paginator.is_prev_page_disabled)
            Assert.false(featured_extensions_page.paginator.is_next_page_disabled)

            featured_extensions_page.paginator.click_prev_page()

            Assert.equal(len(featured_extensions_page.extensions), 20)
            Assert.true(featured_extensions_page.paginator.is_prev_page_disabled)
            Assert.false(featured_extensions_page.paginator.is_next_page_disabled)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_extensions_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        breadcrumbs = featured_extensions_page.breadcrumbs

        Assert.equal(breadcrumbs[0].text, 'Add-ons for Firefox')
        Assert.equal(breadcrumbs[1].text, 'Extensions')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_subscribe_link_exists(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.contains("Subscribe", featured_extensions_page.subscribe_link_text)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_featured_extensions_header(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        Assert.equal("Featured Extensions", featured_extensions_page.featured_extensions_header_text)
