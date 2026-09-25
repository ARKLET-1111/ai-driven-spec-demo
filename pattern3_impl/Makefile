# numlib ビルド・テスト・カバレッジ（AIエージェントはこのファイルを変更しない）
# 使い方: make test / make coverage / make clean
CC      ?= gcc
CFLAGS  ?= -std=c99 -O0 -g -Wall -Wextra -Wpedantic
COV     := --coverage
BUILD   := build

all: test

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/numlib.o: numlib.c numlib.h | $(BUILD)
	$(CC) $(CFLAGS) $(COV) -c numlib.c -o $@

$(BUILD)/test_numlib.o: test_numlib.c numlib.h | $(BUILD)
	$(CC) $(CFLAGS) $(COV) -c test_numlib.c -o $@

$(BUILD)/test_numlib: $(BUILD)/numlib.o $(BUILD)/test_numlib.o
	$(CC) $(COV) -o $@ $^

test: $(BUILD)/test_numlib
	./$(BUILD)/test_numlib

# gcov の生出力を tests/coverage/raw/ に保存。lcov があれば HTML も作る
coverage: test
	gcov -o $(BUILD) numlib.c | tee $(BUILD)/gcov_summary.txt
	mkdir -p tests/coverage/raw && mv -f numlib.c.gcov tests/coverage/raw/ && rm -f *.gcov
	@if command -v lcov >/dev/null 2>&1; then \
	  lcov --quiet --capture --directory $(BUILD) --output-file $(BUILD)/coverage.info --rc branch_coverage=1 && \
	  lcov --quiet --remove $(BUILD)/coverage.info '*/test_*' -o $(BUILD)/coverage.filtered.info && \
	  genhtml --quiet $(BUILD)/coverage.filtered.info -o tests/coverage && echo "HTML: tests/coverage/index.html"; \
	else echo "(lcov なし: tests/coverage/raw/numlib.c.gcov を参照)"; fi

clean:
	rm -rf $(BUILD) *.gcov

.PHONY: all test coverage clean
