#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestCompleteThemes:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_loads_landing_page_correctly(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        url_current_page = complete_themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/complete-themes/"))

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_page_has_correct_title(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        expected_title = "Most Popular Complete Themes :: Add-ons for Firefox"
        Assert.equal(expected_title, complete_themes_page.page_title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_complete_themes_page_breadcrumb(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        expected_breadcrumb = "Complete Themes"
        Assert.equal(expected_breadcrumb, complete_themes_page.breadcrumbs[1].text)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_categories_are_not_extensions_categories(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_categories = complete_themes_page.get_all_categories

        home_page.header.site_navigation_menu("Extensions").click()
        extensions_categories = complete_themes_page.get_all_categories

        Assert.not_equal(len(complete_themes_categories), len(extensions_categories))
        Assert.equal(list(set(complete_themes_categories) & set(extensions_categories)), [])

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_the_displayed_message_for_incompatible_complete_themes(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.clear_hover_cards()

        complete_themes = complete_themes_page.complete_themes

        for complete_theme in complete_themes:
            if complete_theme.is_incompatible:
                Assert.true(complete_theme.is_incompatible_flag_visible)
                Assert.contains('Not available',
                                complete_theme.not_available_flag_text)
            else:
                Assert.false(complete_theme.is_incompatible_flag_visible)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_most_popular_link_is_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        url_current_page = complete_themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/complete-themes/"))
        Assert.equal(complete_themes_page.selected_explore_filter, 'Most Popular')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorted_by_most_users_is_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        url_current_page = complete_themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/complete-themes/"))
        Assert.equal(complete_themes_page.sorted_by, 'Most Users')
