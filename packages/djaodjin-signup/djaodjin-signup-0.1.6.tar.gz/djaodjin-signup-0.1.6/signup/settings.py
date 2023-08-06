# Copyright (c) 2014, Djaodjin Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Convenience module for access of signup app settings, which enforces
default settings when the main settings module does not contain
the appropriate settings.
"""
from django.conf import settings

DISABLED_AUTHENTICATION = getattr(settings, 'DISABLED_AUTHENTICATION', False)

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')
LOGIN_URL = getattr(settings, 'LOGIN_URL')
LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL')

KEY_EXPIRATION = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2)
EMAIL_VERIFICATION_PAT = r'[a-f0-9]{40}'
EMAILER_BACKEND = getattr(settings, 'EMAILER_BACKEND',
                          'signup.backends.django_emailer.TemplateEmailBackend')
