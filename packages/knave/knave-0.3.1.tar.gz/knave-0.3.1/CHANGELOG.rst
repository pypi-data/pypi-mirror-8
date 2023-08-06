Changelog
=========

0.3.1
-----

- Bugfix for issue where roles were incorrectly cached, causing checks
  for roles to fail where they should have passed

0.3
---

- Optimized role membership lookups
- Permission subclasses may now implement custom checking logic
- Added @ACL.role_provider and @role_decider decorators

0.2
---

- Initial release

