#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import random
from copy import deepcopy

from unittestzero import Assert

from pages.desktop.home import Home


class TestAccounts:

    @pytest.mark.nondestructive
    @pytest.mark.login
    @pytest.mark.native
    def test_user_can_login_and_logout(self, mozwebqa, existing_user):
        home_page = Home(mozwebqa)
        home_page.login(existing_user['email'], existing_user['password'])
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_logout()
        Assert.false(home_page.header.is_user_logged_in)

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_user_can_access_the_edit_profile_page(self, mozwebqa, existing_user):
        home_page = Home(mozwebqa)
        home_page.login(existing_user['email'], existing_user['password'])
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.header.is_user_logged_in)

        amo_user_edit_page = home_page.header.click_edit_profile()
        Assert.contains("/users/edit", amo_user_edit_page.get_url_current_page())
        Assert.true(amo_user_edit_page.is_the_current_page)

        Assert.equal("My Account", amo_user_edit_page.account_header_text)
        Assert.equal("Profile", amo_user_edit_page.profile_header_text)
        Assert.equal("Details", amo_user_edit_page.details_header_text)
        Assert.equal("Notifications", amo_user_edit_page.notification_header_text)
