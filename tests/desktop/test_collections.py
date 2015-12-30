#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import time
import uuid

from unittestzero import Assert

from pages.desktop.home import Home
from pages.desktop.details import Details


class TestCollections:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_collections_page = home_page.header.site_navigation_menu("Collections").click()
        Assert.equal(featured_collections_page.default_selected_tab, "Featured")

    @pytest.mark.login
    def test_create_and_delete_collection(self, mozwebqa, existing_user):

        home_page = Home(mozwebqa)
        collections_page = home_page.header.site_navigation_menu('Collections').click()
        create_collection_page = collections_page.click_create_collection_button()
        home_page.login(existing_user['email'], existing_user['password'])

        collection_uuid = uuid.uuid4().hex
        collection_time = repr(time.time())
        collection_name = collection_uuid[:30 - len(collection_time):] + collection_time

        create_collection_page.type_name(collection_name)
        create_collection_page.type_description(collection_name)
        collection = create_collection_page.click_create_collection()

        Assert.equal(collection.notification, 'Collection created!')
        Assert.equal(collection.collection_name, collection_name)
        collection.delete()
        user_collections = collection.delete_confirmation()
        if user_collections.has_no_results:
            pass
        else:
            for collection_element in range(len(user_collections.collections)):  # If the condition is satisfied, iterate through the collections items on the page
                Assert.true(collection_name not in user_collections.collections[collection_element].text)  # Check for each collection that the name is not the same as the deleted collections name
