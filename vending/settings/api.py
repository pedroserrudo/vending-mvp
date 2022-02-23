REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'vending.apps.vauth.authentication.MultipleTokenAuthentication',
    ]
}
