# Flake8 Extension to lint for enforcing doubles

## Usage

If you are using flake8 its as easy as:

```shell
    pip install flake8-doubles
```

When running flake8, simply do:
flake8 --doubles_exceptions='ClassName1,ClassName2'
where ClassName1 and ClassName2 are classes that you don't wish the rule to
apply.
