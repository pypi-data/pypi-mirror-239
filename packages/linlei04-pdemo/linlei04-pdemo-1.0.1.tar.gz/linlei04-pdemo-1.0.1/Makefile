test:
	tox

build:
	rm -rf dist/* && python -m build

# release之前先执行build
release: build
	twine upload dist/*


# Makefile还可以定义变量
a = 1
# 使用时，通过 $(a) 或 ${a} 引用
# a ?= 1 表示a未定义时就定义并赋值1，如果已定义则使用前面定义的指，类似shell里面的a:=1

# 在执行的命令前面加@用于隐藏命令的输出，使输出更加简洁