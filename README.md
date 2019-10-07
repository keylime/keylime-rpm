# Keylime RPM distribution

This reposiory contains SPEC file used for RPM creation of the Keylime Project.

### Contribute

To contibute changes, please clone the repository and create a new branch. Then
push the branch as a pull request.

Before making the Pull Request, please ensure the rpm builds correctly, using the
`rpmbuild -ba python-keylime.spec` and then run `rpmlint keylime-<release>.noarch.rpm`

Ensure no errors are reported.

### Reference

[keylime repository](https://github.com/mit-ll/python-keylime)
