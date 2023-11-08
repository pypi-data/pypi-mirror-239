from setuptools import setup

def remove_comments_and_empty_lines(lines):
        def is_comment_or_empty(line):
            stripped = line.strip()
            return stripped == "" or stripped.startswith("#")

        return [line for line in lines if not is_comment_or_empty(line)]

with open("requirements.txt", "r") as f:
    REQUIREMENTS = remove_comments_and_empty_lines(f.readlines())

setup(
    name="djseong-test-foo",
    version="0.1.1",
    author_email="feedback@gmail.com",
    python_requires=">=3.7",
    install_requires=REQUIREMENTS,
    author="Daniel",
    description="test foo",
)
