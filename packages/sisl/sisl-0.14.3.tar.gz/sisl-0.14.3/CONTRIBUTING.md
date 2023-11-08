# Contributing to sisl
We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## We Develop with GitHub
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

Our repository uses a filter on Jupyter notebooks. So if you are planning on changing notebook content,
you should add this change to your `.git/config`, or in your global `.gitconfig` file:

    [filter "strip-notebook-output"]
        clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"

We also enforce the black style, please run black before committing.

## First-time contributors
Add a comment on the issue and wait for the issue to be assigned before you start working on it. This helps to avoid multiple people working on similar issues.

## We Use [GitHub Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Git-Flow](https://nvie.com/posts/a-successful-git-branching-model/)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`. Please create the branch in the format feature/<issue-id>-<issue-name> (eg: feature/176-chart-widget)
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Issue that pull request!

## Any contributions you make will be under the MPL v2 License
In short, when you submit code changes, your submissions are understood to be under the same [MPL v2 License](https://www.mozilla.org/en-US/MPL/2.0) that covers the project.

## Report bugs using GitHub's [issues](https://github.com/zerothi/sisl/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/zerothi/sisl/issues/new/choose). It's that easy!

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License
By contributing, you agree that your contributions will be licensed under its MPL v2 License.

## Questions? 
Contact us on discord [Discord](https://discord.gg/5XnFXFdkv2).
