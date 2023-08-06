# Release notes

## 0.2.1 (2014-12-20)

- changed type checking keyword argument names: `opt` -> `or_none`
  and `nodups` -> `unique`
- improved error messages for constructing Structs
- significant updates to readme and examples
- using `opt=True` on `TypedField` no longer implies that `None` is
  the default value
- made mixin version of `checktype()` and `checktype_seq()`
- added `check()` and `normalize()` hooks to `TypedField`
- accessing fields descriptors from classes is now permissible
- added support for default values in general, and optional values
  for type-checked fields
- fixed `__repr__()` on recursive Structs

## 0.2.0 (2014-12-15)

- initial release
