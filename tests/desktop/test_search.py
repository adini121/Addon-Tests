#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.home import Home


class TestSearch:

    @pytest.mark.nondestructive
    def test_that_page_with_search_results_has_correct_title(self, mozwebqa):
        home_page = Home(mozwebqa)
        search_keyword = 'Search term'
        search_page = home_page.search_for(search_keyword)

        expected_title = '%s :: Search :: Add-ons for Firefox' % search_keyword
        Assert.equal(expected_title, search_page.page_title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_newest(self, mozwebqa):
        search_page = Home(mozwebqa).search_for('firebug')
        search_page.click_sort_by('Newest')
        Assert.true('sort=created' in search_page.get_url_current_page())
        Assert.is_sorted_descending([i.created_date for i in search_page.results])

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorting_by_number_of_most_users(self, mozwebqa):
        search_page = Home(mozwebqa).search_for('firebug')
        search_page.click_sort_by('Most Users')
        Assert.contains('sort=users', search_page.get_url_current_page())
        Assert.is_sorted_descending([i.users for i in search_page.results])

