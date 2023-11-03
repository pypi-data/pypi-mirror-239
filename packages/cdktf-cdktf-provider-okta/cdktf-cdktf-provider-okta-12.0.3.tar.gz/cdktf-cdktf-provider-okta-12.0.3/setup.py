import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-okta",
    "version": "12.0.3",
    "description": "Prebuilt okta Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-okta.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-okta.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_okta",
        "cdktf_cdktf_provider_okta._jsii",
        "cdktf_cdktf_provider_okta.admin_role_custom",
        "cdktf_cdktf_provider_okta.admin_role_custom_assignments",
        "cdktf_cdktf_provider_okta.admin_role_targets",
        "cdktf_cdktf_provider_okta.app_access_policy_assignment",
        "cdktf_cdktf_provider_okta.app_auto_login",
        "cdktf_cdktf_provider_okta.app_basic_auth",
        "cdktf_cdktf_provider_okta.app_bookmark",
        "cdktf_cdktf_provider_okta.app_group_assignment",
        "cdktf_cdktf_provider_okta.app_group_assignments",
        "cdktf_cdktf_provider_okta.app_oauth",
        "cdktf_cdktf_provider_okta.app_oauth_api_scope",
        "cdktf_cdktf_provider_okta.app_oauth_post_logout_redirect_uri",
        "cdktf_cdktf_provider_okta.app_oauth_redirect_uri",
        "cdktf_cdktf_provider_okta.app_oauth_role_assignment",
        "cdktf_cdktf_provider_okta.app_saml",
        "cdktf_cdktf_provider_okta.app_saml_app_settings",
        "cdktf_cdktf_provider_okta.app_secure_password_store",
        "cdktf_cdktf_provider_okta.app_shared_credentials",
        "cdktf_cdktf_provider_okta.app_signon_policy",
        "cdktf_cdktf_provider_okta.app_signon_policy_rule",
        "cdktf_cdktf_provider_okta.app_swa",
        "cdktf_cdktf_provider_okta.app_three_field",
        "cdktf_cdktf_provider_okta.app_user",
        "cdktf_cdktf_provider_okta.app_user_base_schema_property",
        "cdktf_cdktf_provider_okta.app_user_schema_property",
        "cdktf_cdktf_provider_okta.auth_server",
        "cdktf_cdktf_provider_okta.auth_server_claim",
        "cdktf_cdktf_provider_okta.auth_server_claim_default",
        "cdktf_cdktf_provider_okta.auth_server_default",
        "cdktf_cdktf_provider_okta.auth_server_policy",
        "cdktf_cdktf_provider_okta.auth_server_policy_rule",
        "cdktf_cdktf_provider_okta.auth_server_scope",
        "cdktf_cdktf_provider_okta.authenticator",
        "cdktf_cdktf_provider_okta.behavior",
        "cdktf_cdktf_provider_okta.brand",
        "cdktf_cdktf_provider_okta.captcha",
        "cdktf_cdktf_provider_okta.captcha_org_wide_settings",
        "cdktf_cdktf_provider_okta.data_okta_app",
        "cdktf_cdktf_provider_okta.data_okta_app_group_assignments",
        "cdktf_cdktf_provider_okta.data_okta_app_metadata_saml",
        "cdktf_cdktf_provider_okta.data_okta_app_oauth",
        "cdktf_cdktf_provider_okta.data_okta_app_saml",
        "cdktf_cdktf_provider_okta.data_okta_app_signon_policy",
        "cdktf_cdktf_provider_okta.data_okta_app_user_assignments",
        "cdktf_cdktf_provider_okta.data_okta_auth_server",
        "cdktf_cdktf_provider_okta.data_okta_auth_server_claim",
        "cdktf_cdktf_provider_okta.data_okta_auth_server_claims",
        "cdktf_cdktf_provider_okta.data_okta_auth_server_policy",
        "cdktf_cdktf_provider_okta.data_okta_auth_server_scopes",
        "cdktf_cdktf_provider_okta.data_okta_authenticator",
        "cdktf_cdktf_provider_okta.data_okta_behavior",
        "cdktf_cdktf_provider_okta.data_okta_behaviors",
        "cdktf_cdktf_provider_okta.data_okta_brand",
        "cdktf_cdktf_provider_okta.data_okta_brands",
        "cdktf_cdktf_provider_okta.data_okta_default_policy",
        "cdktf_cdktf_provider_okta.data_okta_domain",
        "cdktf_cdktf_provider_okta.data_okta_email_customization",
        "cdktf_cdktf_provider_okta.data_okta_email_customizations",
        "cdktf_cdktf_provider_okta.data_okta_email_template",
        "cdktf_cdktf_provider_okta.data_okta_email_templates",
        "cdktf_cdktf_provider_okta.data_okta_everyone_group",
        "cdktf_cdktf_provider_okta.data_okta_group",
        "cdktf_cdktf_provider_okta.data_okta_group_rule",
        "cdktf_cdktf_provider_okta.data_okta_groups",
        "cdktf_cdktf_provider_okta.data_okta_idp_metadata_saml",
        "cdktf_cdktf_provider_okta.data_okta_idp_oidc",
        "cdktf_cdktf_provider_okta.data_okta_idp_saml",
        "cdktf_cdktf_provider_okta.data_okta_idp_social",
        "cdktf_cdktf_provider_okta.data_okta_network_zone",
        "cdktf_cdktf_provider_okta.data_okta_org_metadata",
        "cdktf_cdktf_provider_okta.data_okta_policy",
        "cdktf_cdktf_provider_okta.data_okta_role_subscription",
        "cdktf_cdktf_provider_okta.data_okta_theme",
        "cdktf_cdktf_provider_okta.data_okta_themes",
        "cdktf_cdktf_provider_okta.data_okta_trusted_origins",
        "cdktf_cdktf_provider_okta.data_okta_user",
        "cdktf_cdktf_provider_okta.data_okta_user_profile_mapping_source",
        "cdktf_cdktf_provider_okta.data_okta_user_security_questions",
        "cdktf_cdktf_provider_okta.data_okta_user_type",
        "cdktf_cdktf_provider_okta.data_okta_users",
        "cdktf_cdktf_provider_okta.domain",
        "cdktf_cdktf_provider_okta.domain_certificate",
        "cdktf_cdktf_provider_okta.domain_verification",
        "cdktf_cdktf_provider_okta.email_customization",
        "cdktf_cdktf_provider_okta.email_domain",
        "cdktf_cdktf_provider_okta.email_domain_verification",
        "cdktf_cdktf_provider_okta.email_sender",
        "cdktf_cdktf_provider_okta.email_sender_verification",
        "cdktf_cdktf_provider_okta.event_hook",
        "cdktf_cdktf_provider_okta.event_hook_verification",
        "cdktf_cdktf_provider_okta.factor",
        "cdktf_cdktf_provider_okta.factor_totp",
        "cdktf_cdktf_provider_okta.group",
        "cdktf_cdktf_provider_okta.group_memberships",
        "cdktf_cdktf_provider_okta.group_role",
        "cdktf_cdktf_provider_okta.group_rule",
        "cdktf_cdktf_provider_okta.group_schema_property",
        "cdktf_cdktf_provider_okta.idp_oidc",
        "cdktf_cdktf_provider_okta.idp_saml",
        "cdktf_cdktf_provider_okta.idp_saml_key",
        "cdktf_cdktf_provider_okta.idp_social",
        "cdktf_cdktf_provider_okta.inline_hook",
        "cdktf_cdktf_provider_okta.link_definition",
        "cdktf_cdktf_provider_okta.link_value",
        "cdktf_cdktf_provider_okta.network_zone",
        "cdktf_cdktf_provider_okta.org_configuration",
        "cdktf_cdktf_provider_okta.org_support",
        "cdktf_cdktf_provider_okta.policy_device_assurance_android",
        "cdktf_cdktf_provider_okta.policy_device_assurance_chromeos",
        "cdktf_cdktf_provider_okta.policy_device_assurance_ios",
        "cdktf_cdktf_provider_okta.policy_device_assurance_macos",
        "cdktf_cdktf_provider_okta.policy_device_assurance_windows",
        "cdktf_cdktf_provider_okta.policy_mfa",
        "cdktf_cdktf_provider_okta.policy_mfa_default",
        "cdktf_cdktf_provider_okta.policy_password",
        "cdktf_cdktf_provider_okta.policy_password_default",
        "cdktf_cdktf_provider_okta.policy_profile_enrollment",
        "cdktf_cdktf_provider_okta.policy_profile_enrollment_apps",
        "cdktf_cdktf_provider_okta.policy_rule_idp_discovery",
        "cdktf_cdktf_provider_okta.policy_rule_mfa",
        "cdktf_cdktf_provider_okta.policy_rule_password",
        "cdktf_cdktf_provider_okta.policy_rule_profile_enrollment",
        "cdktf_cdktf_provider_okta.policy_rule_signon",
        "cdktf_cdktf_provider_okta.policy_signon",
        "cdktf_cdktf_provider_okta.profile_mapping",
        "cdktf_cdktf_provider_okta.provider",
        "cdktf_cdktf_provider_okta.rate_limiting",
        "cdktf_cdktf_provider_okta.resource_set",
        "cdktf_cdktf_provider_okta.role_subscription",
        "cdktf_cdktf_provider_okta.security_notification_emails",
        "cdktf_cdktf_provider_okta.template_sms",
        "cdktf_cdktf_provider_okta.theme",
        "cdktf_cdktf_provider_okta.threat_insight_settings",
        "cdktf_cdktf_provider_okta.trusted_origin",
        "cdktf_cdktf_provider_okta.user",
        "cdktf_cdktf_provider_okta.user_admin_roles",
        "cdktf_cdktf_provider_okta.user_base_schema_property",
        "cdktf_cdktf_provider_okta.user_factor_question",
        "cdktf_cdktf_provider_okta.user_group_memberships",
        "cdktf_cdktf_provider_okta.user_schema_property",
        "cdktf_cdktf_provider_okta.user_type"
    ],
    "package_data": {
        "cdktf_cdktf_provider_okta._jsii": [
            "provider-okta@12.0.3.jsii.tgz"
        ],
        "cdktf_cdktf_provider_okta": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.19.0, <0.20.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.91.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
