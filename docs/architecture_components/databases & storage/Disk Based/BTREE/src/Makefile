.PHONY: help install fmt vet test bench lint clean pre-commit

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install dependencies and pre-commit hooks"
	@echo "  fmt          - Format code with gofmt and goimports"
	@echo "  vet          - Run go vet"
	@echo "  test         - Run tests"
	@echo "  bench        - Run benchmarks"
	@echo "  lint         - Run golangci-lint"
	@echo "  clean        - Clean build artifacts"
	@echo "  pre-commit   - Run pre-commit hooks manually"

install:
	go mod download
	go install golang.org/x/tools/cmd/goimports@latest
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	pre-commit install

fmt:
	gofmt -s -w .
	goimports -w .

vet:
	go vet ./...

test:
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

bench:
	go test -bench=. -benchmem -cpuprofile=cpu.prof -memprofile=mem.prof ./...

lint:
	golangci-lint run --timeout 5m

clean:
	go clean
	rm -f coverage.out coverage.html cpu.prof mem.prof

pre-commit:
	pre-commit run --all-files
