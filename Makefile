.PHONY: all build check cpp python rust api integration clean

all: check

build:
	./scripts/build.sh

check:
	./scripts/check.sh

cpp:
	cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
	cmake --build build
	ctest --test-dir build --output-on-failure

python:
	PYTHONPATH=tools/ingest-py python3 -m unittest discover -s tools/ingest-py/tests -v

rust:
	cargo test --manifest-path services/search-rs/Cargo.toml

api:
	node --experimental-strip-types --test apps/api-ts/test/*.test.ts

integration:
	./scripts/integration-check.sh

clean:
	rm -rf build services/search-rs/target data/generated.atlas
